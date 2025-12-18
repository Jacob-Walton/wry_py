use crate::elements::Element;
use crate::renderer::render_to_html;
use parking_lot::Mutex;
use pyo3::prelude::*;
use std::collections::HashMap;
use std::sync::Arc;
use tao::event::{Event, WindowEvent};
use tao::event_loop::{ControlFlow, EventLoop, EventLoopBuilder, EventLoopProxy};
use tao::window::WindowBuilder;
use wry::WebViewBuilder;

/// Custom events we can send to the event loop
#[derive(Debug, Clone)]
pub enum UserEvent {
    UpdateRoot(String), // HTML content
    SetTitle(String),
    Close,
}

/// Shared state between Python and the webview
struct WebViewState {
    callbacks: HashMap<String, Py<PyAny>>,
    pending_html: Option<String>,
}

impl WebViewState {
    fn new() -> Self {
        WebViewState {
            callbacks: HashMap::new(),
            pending_html: None,
        }
    }
}

/// Main window class exposed to Python
#[pyclass]
pub struct UiWindow {
    title: String,
    width: u32,
    height: u32,
    event_proxy: Arc<Mutex<Option<EventLoopProxy<UserEvent>>>>,
    state: Arc<Mutex<WebViewState>>,
    is_running: Arc<Mutex<bool>>,
    background_color: (u8, u8, u8, u8),
}

#[pymethods]
impl UiWindow {
    #[new]
    #[pyo3(signature = (title = None, width = None, height = None, background_color = None))]
    fn new(
        title: Option<String>,
        width: Option<u32>,
        height: Option<u32>,
        background_color: Option<String>,
    ) -> Self {
        let bg = background_color
            .and_then(|c| parse_hex_color(&c))
            .unwrap_or((26, 26, 26, 255)); // Default: #1a1a1a

        UiWindow {
            title: title.unwrap_or_else(|| "Python App".to_string()),
            width: width.unwrap_or(800),
            height: height.unwrap_or(600),
            event_proxy: Arc::new(Mutex::new(None)),
            state: Arc::new(Mutex::new(WebViewState::new())),
            is_running: Arc::new(Mutex::new(false)),
            background_color: bg,
        }
    }

    /// Set the root element and update the webview
    fn set_root(&self, element: &Element) -> PyResult<()> {
        // Register callbacks from element
        let html = {
            let mut state = self.state.lock();
            for (id, callback) in element.collect_callbacks() {
                state.callbacks.insert(id, callback);
            }

            // Render element to HTML
            let html = render_to_html(&element.def);

            // Store as pending if not running yet
            state.pending_html = Some(html.clone());
            html
        };

        // Send update to webview if already running
        if let Some(proxy) = self.event_proxy.lock().as_ref() {
            let _ = proxy.send_event(UserEvent::UpdateRoot(html));
        }

        Ok(())
    }

    /// Set window title
    fn set_title(&self, title: String) -> PyResult<()> {
        if let Some(proxy) = self.event_proxy.lock().as_ref() {
            let _ = proxy.send_event(UserEvent::SetTitle(title));
        }
        Ok(())
    }

    /// Run the window event loop (blocking)
    fn run(&self, py: Python) -> PyResult<()> {
        let title = self.title.clone();
        let width = self.width;
        let height = self.height;
        let state = self.state.clone();
        let event_proxy_holder = self.event_proxy.clone();
        let is_running = self.is_running.clone();
        let background_color = self.background_color;

        // Release GIL while running the event loop
        #[allow(deprecated)]
        py.allow_threads(|| {
            run_event_loop(title, width, height, state, event_proxy_holder, is_running, background_color)
        })
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
    }

    /// Close the window
    fn close(&self) -> PyResult<()> {
        if let Some(proxy) = self.event_proxy.lock().as_ref() {
            let _ = proxy.send_event(UserEvent::Close);
        }
        Ok(())
    }

    /// Check if window is running
    fn is_running(&self) -> bool {
        *self.is_running.lock()
    }

    fn __repr__(&self) -> String {
        format!(
            "UiWindow(title='{}', size={}x{})",
            self.title, self.width, self.height
        )
    }
}

fn run_event_loop(
    title: String,
    width: u32,
    height: u32,
    state: Arc<Mutex<WebViewState>>,
    event_proxy_holder: Arc<Mutex<Option<EventLoopProxy<UserEvent>>>>,
    is_running: Arc<Mutex<bool>>,
    background_color: (u8, u8, u8, u8),
) -> Result<(), String> {
    // NVIDIA + Wayland workaround
    #[cfg(target_os = "linux")]
    {
        if std::path::Path::new("/dev/dri").exists()
            && std::env::var("WAYLAND_DISPLAY").is_ok()
            && std::env::var("XDG_SESSION_TYPE").unwrap_or_default() == "wayland"
        {
            unsafe {
                std::env::set_var("__NV_DISABLE_EXPLICIT_SYNC", "1");
            }
        }
    }

    let event_loop: EventLoop<UserEvent> = EventLoopBuilder::with_user_event().build();

    // Store the proxy so Python can send events
    *event_proxy_holder.lock() = Some(event_loop.create_proxy());
    *is_running.lock() = true;

    let window = WindowBuilder::new()
        .with_title(&title)
        .with_inner_size(tao::dpi::LogicalSize::new(width, height))
        .build(&event_loop)
        .map_err(|e| e.to_string())?;

    // Get pending HTML or use default
    let initial_content = {
        let state = state.lock();
        state.pending_html.clone()
    };

    let initial_html = get_initial_html(initial_content.as_deref(), background_color);

    // Create IPC handler for callbacks
    let state_clone = state.clone();
    let _proxy_for_callbacks = event_loop.create_proxy();

    let ipc_handler = move |request: wry::http::Request<String>| {
        let body = request.body();
        if let Ok(event) = serde_json::from_str::<IpcEvent>(body) {
            if event.event_type == "click" {
                if let Some(ref callback_id) = event.callback_id {
                    let state_for_cb = state_clone.clone();
                    let callback_id = callback_id.clone();
                    #[allow(deprecated)]
                    Python::with_gil(|py| {
                        let callback = {
                            let state = state_for_cb.lock();
                            state.callbacks.get(&callback_id).map(|cb| cb.clone_ref(py))
                        };

                        if let Some(callback) = callback {
                            std::thread::spawn(move || {
                                #[allow(deprecated)]
                                Python::with_gil(|py| {
                                    if let Err(e) = callback.call0(py) {
                                        eprintln!("Callback error: {:?}", e);
                                    }
                                });
                            });
                        }
                    });
                }
            }

            if event.event_type == "input" {
                if let (Some(callback_id), Some(value)) = (&event.callback_id, event.value) {
                    let state_for_cb = state_clone.clone();
                    let callback_id = callback_id.clone();
                    #[allow(deprecated)]
                    Python::with_gil(|py| {
                        let callback = {
                            let state = state_for_cb.lock();
                            state.callbacks.get(&callback_id).map(|cb| cb.clone_ref(py))
                        };

                        if let Some(callback) = callback {
                            std::thread::spawn(move || {
                                #[allow(deprecated)]
                                Python::with_gil(|py| {
                                    if let Err(e) = callback.call1(py, (value,)) {
                                        eprintln!("Input callback error: {:?}", e);
                                    }
                                });
                            });
                        }
                    });
                }
            }
        }
    };

    let webview = WebViewBuilder::new()
        .with_html(initial_html)
        .with_ipc_handler(ipc_handler)
        .with_background_color(background_color)
        .build(&window)
        .map_err(|e| e.to_string())?;

    {
        let state = state.lock();
        if let Some(ref html) = state.pending_html {
            let js = format!("document.getElementById('root').innerHTML = `{}`;", html.replace('`', "\\`"));
            let _ = webview.evaluate_script(&js);
        }
    }

    event_loop.run(move |event, _, control_flow| {
        *control_flow = ControlFlow::Wait;

        match event {
            Event::WindowEvent {
                event: WindowEvent::CloseRequested,
                ..
            } => {
                *is_running.lock() = false;
                *control_flow = ControlFlow::Exit;
            }

            Event::UserEvent(user_event) => match user_event {
                UserEvent::UpdateRoot(html) => {
                    let js = format!(
                        "document.getElementById('root').innerHTML = {};",
                        serde_json::to_string(&html).unwrap()
                    );
                    let _ = webview.evaluate_script(&js);
                }
                UserEvent::SetTitle(title) => {
                    window.set_title(&title);
                }
                UserEvent::Close => {
                    *is_running.lock() = false;
                    *control_flow = ControlFlow::Exit;
                }
            },

            _ => {}
        }
    });

    #[allow(unreachable_code)]
    {
        *event_proxy_holder.lock() = None;
        Ok(())
    }
}

#[derive(serde::Deserialize)]
struct IpcEvent {
    event_type: String,
    callback_id: Option<String>,
    value: Option<String>,
}

/// Parse a hex color string like "#1a1a1a" or "#1a1a1aff" to RGBA tuple
fn parse_hex_color(hex: &str) -> Option<(u8, u8, u8, u8)> {
    let hex = hex.trim_start_matches('#');
    match hex.len() {
        6 => {
            let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
            let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
            let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
            Some((r, g, b, 255))
        }
        8 => {
            let r = u8::from_str_radix(&hex[0..2], 16).ok()?;
            let g = u8::from_str_radix(&hex[2..4], 16).ok()?;
            let b = u8::from_str_radix(&hex[4..6], 16).ok()?;
            let a = u8::from_str_radix(&hex[6..8], 16).ok()?;
            Some((r, g, b, a))
        }
        _ => None,
    }
}

fn get_initial_html(content: Option<&str>, background_color: (u8, u8, u8, u8)) -> String {
    let root_content = content.unwrap_or(r#"<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#666;">Loading...</div>"#);
    let (r, g, b, _a) = background_color;

    format!(
        r#"<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: rgb({}, {}, {});
            color: #ffffff;
            min-height: 100vh;
        }}
        #root {{
            width: 100%;
            height: 100vh;
        }}
        .size-full {{
            width: 100%;
            height: 100%;
        }}
        .flex-row {{ display: flex; flex-direction: row; }}
        .flex-col {{ display: flex; flex-direction: column; }}
        .items-center {{ align-items: center; }}
        .items-start {{ align-items: flex-start; }}
        .items-end {{ align-items: flex-end; }}
        .justify-center {{ justify-content: center; }}
        .justify-between {{ justify-content: space-between; }}
        .justify-start {{ justify-content: flex-start; }}
        .justify-end {{ justify-content: flex-end; }}
    </style>
</head>
<body>
    <div id="root">{}</div>
    <script>
        function handleClick(callbackId) {{
            window.ipc.postMessage(JSON.stringify({{
                event_type: 'click',
                callback_id: callbackId
            }}));
        }}

        function handleInput(callbackId, value) {{
            window.ipc.postMessage(JSON.stringify({{
                event_type: 'input',
                callback_id: callbackId,
                value: value
            }}));
        }}

    </script>
</body>
</html>"#,
        r, g, b, root_content
    )
}
