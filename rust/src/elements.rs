use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;

/// Serializable element definition sent to frontend.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ElementDef {
    pub id: String,
    pub element_type: String,

    // Layout
    #[serde(skip_serializing_if = "Option::is_none")]
    pub width: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub height: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flex_direction: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub align_items: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub justify_content: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub gap: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub padding: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub padding_top: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub padding_right: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub padding_bottom: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub padding_left: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub margin: Option<f32>,
    pub size_full: bool,

    // Styling
    #[serde(skip_serializing_if = "Option::is_none")]
    pub background_color: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub text_color: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub border_radius: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub border_width: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub border_color: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub overflow: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub text_align: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub word_wrap: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub position: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub top: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub right: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub bottom: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub left: Option<f32>,

    // Text
    #[serde(skip_serializing_if = "Option::is_none")]
    pub text_content: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub font_size: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub font_weight: Option<String>,

    // Interactivity
    #[serde(skip_serializing_if = "Option::is_none")]
    pub on_click: Option<String>, // callback ID
    #[serde(skip_serializing_if = "Option::is_none")]
    pub on_input: Option<String>, // callback ID for input changes
    #[serde(skip_serializing_if = "Option::is_none")]
    pub value: Option<String>, // input value
    #[serde(skip_serializing_if = "Option::is_none")]
    pub placeholder: Option<String>,

    // Children
    #[serde(default)]
    pub children: Vec<ElementDef>,
}

impl Default for ElementDef {
    fn default() -> Self {
        Self {
            id: uuid(),
            element_type: "div".to_string(),
            width: None,
            height: None,
            flex_direction: None,
            align_items: None,
            justify_content: None,
            gap: None,
            padding: None,
            padding_top: None,
            padding_right: None,
            padding_bottom: None,
            padding_left: None,
            margin: None,
            size_full: false,
            background_color: None,
            text_color: None,
            border_radius: None,
            border_width: None,
            border_color: None,
            overflow: None,
            text_align: None,
            word_wrap: None,
            position: None,
            top: None,
            right: None,
            bottom: None,
            left: None,
            text_content: None,
            font_size: None,
            font_weight: None,
            on_click: None,
            on_input: None,
            value: None,
            placeholder: None,
            children: Vec::new(),
        }
    }
}

fn uuid() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    static COUNTER: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
    let count = COUNTER.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    format!("el_{:x}_{}", nanos, count)
}

// Global callback store
static CALLBACK_STORE: Mutex<Option<HashMap<String, Py<PyAny>>>> = Mutex::new(None);

fn init_callback_store() {
    let mut store = CALLBACK_STORE.lock().unwrap();
    if store.is_none() {
        *store = Some(HashMap::new());
    }
}

fn store_callback(id: String, callback: Py<PyAny>) {
    init_callback_store();
    let mut store = CALLBACK_STORE.lock().unwrap();
    if let Some(ref mut map) = *store {
        map.insert(id, callback);
    }
}

pub fn take_callbacks() -> HashMap<String, Py<PyAny>> {
    init_callback_store();
    let mut store = CALLBACK_STORE.lock().unwrap();
    store.take().unwrap_or_default()
}

/// Python Element class
#[pyclass]
#[derive(Clone)]
pub struct Element {
    pub def: ElementDef,
    callback_ids: Vec<String>,
}

#[pymethods]
impl Element {
    #[new]
    fn new(element_type: Option<String>) -> Self {
        let mut def = ElementDef::default();
        if let Some(t) = element_type {
            def.element_type = t;
        }
        Element {
            def,
            callback_ids: Vec::new(),
        }
    }

    fn to_json(&self) -> PyResult<String> {
        serde_json::to_string(&self.def)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))
    }

    fn __repr__(&self) -> String {
        format!(
            "Element(type='{}', children={})",
            self.def.element_type,
            self.def.children.len()
        )
    }
}

impl Element {
    pub fn collect_callbacks(&self) -> HashMap<String, Py<PyAny>> {
        take_callbacks()
    }
}

/// Builder pattern for creating elements
#[pyclass]
#[derive(Clone)]
pub struct ElementBuilder {
    element: Element,
}

#[pymethods]
impl ElementBuilder {
    #[staticmethod]
    fn div() -> Self {
        ElementBuilder {
            element: Element::new(Some("div".to_string())),
        }
    }

    #[staticmethod]
    fn text(content: String) -> Self {
        let mut element = Element::new(Some("text".to_string()));
        element.def.text_content = Some(content);
        ElementBuilder { element }
    }

    #[staticmethod]
    fn button(label: String) -> Self {
        let mut element = Element::new(Some("button".to_string()));
        element.def.text_content = Some(label);
        ElementBuilder { element }
    }

    #[staticmethod]
    fn image(src: String) -> Self {
        let mut element = Element::new(Some("image".to_string()));
        element.def.text_content = Some(src);
        ElementBuilder { element }
    }

    #[staticmethod]
    fn input() -> Self {
        ElementBuilder {
            element: Element::new(Some("input".to_string())),
        }
    }

    /// Set width in pixels
    fn width(mut slf: PyRefMut<'_, Self>, w: f32) -> PyRefMut<'_, Self> {
        slf.element.def.width = Some(w);
        slf
    }

    /// Set height in pixels
    fn height(mut slf: PyRefMut<'_, Self>, h: f32) -> PyRefMut<'_, Self> {
        slf.element.def.height = Some(h);
        slf
    }

    /// Set both width and height
    fn size(mut slf: PyRefMut<'_, Self>, w: f32, h: f32) -> PyRefMut<'_, Self> {
        slf.element.def.width = Some(w);
        slf.element.def.height = Some(h);
        slf
    }

    /// Make element fill available space
    fn size_full(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.size_full = true;
        slf
    }

    /// Vertical flex layout
    fn v_flex(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.flex_direction = Some("column".to_string());
        slf
    }

    /// Horizontal flex layout
    fn h_flex(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.flex_direction = Some("row".to_string());
        slf
    }

    /// Center items on cross axis
    fn items_center(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.align_items = Some("center".to_string());
        slf
    }

    /// Center content on main axis
    fn justify_center(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.justify_content = Some("center".to_string());
        slf
    }

    /// Space between items
    fn justify_between(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.justify_content = Some("space-between".to_string());
        slf
    }

    /// Set gap between children
    fn gap(mut slf: PyRefMut<'_, Self>, g: f32) -> PyRefMut<'_, Self> {
        slf.element.def.gap = Some(g);
        slf
    }

    /// Set padding
    fn padding(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding = Some(p);
        slf
    }

    /// Alias for padding
    fn p(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding = Some(p);
        slf
    }

    /// Set padding top
    fn pt(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_top = Some(p);
        slf
    }

    /// Set padding right
    fn pr(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_right = Some(p);
        slf
    }

    /// Set padding bottom
    fn pb(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_bottom = Some(p);
        slf
    }

    /// Set padding left
    fn pl(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_left = Some(p);
        slf
    }

    /// Set padding x (left and right)
    fn px(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_left = Some(p);
        slf.element.def.padding_right = Some(p);
        slf
    }

    /// Set padding y (top and bottom)
    fn py(mut slf: PyRefMut<'_, Self>, p: f32) -> PyRefMut<'_, Self> {
        slf.element.def.padding_top = Some(p);
        slf.element.def.padding_bottom = Some(p);
        slf
    }

    /// Set margin
    fn margin(mut slf: PyRefMut<'_, Self>, m: f32) -> PyRefMut<'_, Self> {
        slf.element.def.margin = Some(m);
        slf
    }

    /// Alias for margin
    fn m(mut slf: PyRefMut<'_, Self>, m: f32) -> PyRefMut<'_, Self> {
        slf.element.def.margin = Some(m);
        slf
    }

    /// Set background color (hex string like "#ff0000" or "rgb(255,0,0)")
    fn bg(mut slf: PyRefMut<'_, Self>, color: String) -> PyRefMut<'_, Self> {
        slf.element.def.background_color = Some(color);
        slf
    }

    /// Set text color
    fn text_color(mut slf: PyRefMut<'_, Self>, color: String) -> PyRefMut<'_, Self> {
        slf.element.def.text_color = Some(color);
        slf
    }

    /// Set border radius (rounded corners)
    fn rounded(mut slf: PyRefMut<'_, Self>, radius: f32) -> PyRefMut<'_, Self> {
        slf.element.def.border_radius = Some(radius);
        slf
    }

    /// Set border
    fn border(mut slf: PyRefMut<'_, Self>, width: f32, color: String) -> PyRefMut<'_, Self> {
        slf.element.def.border_width = Some(width);
        slf.element.def.border_color = Some(color);
        slf
    }

    /// Short alias for border (1px solid color)
    fn b(mut slf: PyRefMut<'_, Self>, color: String) -> PyRefMut<'_, Self> {
        slf.element.def.border_width = Some(1.0);
        slf.element.def.border_color = Some(color);
        slf
    }

    /// Set overflow to hidden
    fn overflow_hidden(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.overflow = Some("hidden".to_string());
        slf
    }

    /// Set overflow
    fn overflow(mut slf: PyRefMut<'_, Self>, value: String) -> PyRefMut<'_, Self> {
        slf.element.def.overflow = Some(value);
        slf
    }

    /// Set text alignment
    fn text_align(mut slf: PyRefMut<'_, Self>, align: String) -> PyRefMut<'_, Self> {
        slf.element.def.text_align = Some(align);
        slf
    }

    /// Center text
    fn text_center(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.text_align = Some("center".to_string());
        slf
    }

    /// Set word wrap
    fn word_wrap(mut slf: PyRefMut<'_, Self>, value: String) -> PyRefMut<'_, Self> {
        slf.element.def.word_wrap = Some(value);
        slf
    }

    /// Set position
    fn position(mut slf: PyRefMut<'_, Self>, value: String) -> PyRefMut<'_, Self> {
        slf.element.def.position = Some(value);
        slf
    }

    /// Set position to absolute
    fn absolute(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.position = Some("absolute".to_string());
        slf
    }

    /// Set position to relative
    fn relative(mut slf: PyRefMut<'_, Self>) -> PyRefMut<'_, Self> {
        slf.element.def.position = Some("relative".to_string());
        slf
    }

    /// Set top position
    fn top(mut slf: PyRefMut<'_, Self>, value: f32) -> PyRefMut<'_, Self> {
        slf.element.def.top = Some(value);
        slf
    }

    /// Set right position
    fn right(mut slf: PyRefMut<'_, Self>, value: f32) -> PyRefMut<'_, Self> {
        slf.element.def.right = Some(value);
        slf
    }

    /// Set bottom position
    fn bottom(mut slf: PyRefMut<'_, Self>, value: f32) -> PyRefMut<'_, Self> {
        slf.element.def.bottom = Some(value);
        slf
    }

    /// Set left position
    fn left(mut slf: PyRefMut<'_, Self>, value: f32) -> PyRefMut<'_, Self> {
        slf.element.def.left = Some(value);
        slf
    }

    /// Set font size
    fn text_size(mut slf: PyRefMut<'_, Self>, size: f32) -> PyRefMut<'_, Self> {
        slf.element.def.font_size = Some(size);
        slf
    }

    /// Set font weight ("normal", "bold", "100"-"900")
    fn text_weight(mut slf: PyRefMut<'_, Self>, weight: String) -> PyRefMut<'_, Self> {
        slf.element.def.font_weight = Some(weight);
        slf
    }

    /// Add a child element
    fn child(&mut self, child: &Element) -> Self {
        self.element.def.children.push(child.def.clone());
        self.element.callback_ids.extend(child.callback_ids.clone());
        self.clone()
    }

    /// Add a child from a builder
    fn child_builder(&mut self, child: &ElementBuilder) -> Self {
        self.element.def.children.push(child.element.def.clone());
        self.element.callback_ids.extend(child.element.callback_ids.clone());
        self.clone()
    }

    /// Add text child (convenience)
    fn child_text(mut slf: PyRefMut<'_, Self>, text: String) -> PyRefMut<'_, Self> {
        let mut text_def = ElementDef::default();
        text_def.element_type = "text".to_string();
        text_def.text_content = Some(text);
        slf.element.def.children.push(text_def);
        slf
    }

    /// Set click handler
    fn on_click(&mut self, callback: Py<PyAny>) -> Self {
        let callback_id = uuid();
        self.element.def.on_click = Some(callback_id.clone());
        self.element.callback_ids.push(callback_id.clone());
        store_callback(callback_id, callback);
        self.clone()
    }

    /// Set input value
    fn value(mut slf: PyRefMut<'_, Self>, val: String) -> PyRefMut<'_, Self> {
        slf.element.def.value = Some(val);
        slf
    }

    /// Set placeholder text
    fn placeholder(mut slf: PyRefMut<'_, Self>, text: String) -> PyRefMut<'_, Self> {
        slf.element.def.placeholder = Some(text);
        slf
    }

    /// Set input handler
    fn on_input(&mut self, callback: Py<PyAny>) -> Self {
        let callback_id = uuid();
        self.element.def.on_input = Some(callback_id.clone());
        self.element.callback_ids.push(callback_id.clone());
        store_callback(callback_id, callback);
        self.clone()
    }

    /// Build and return the element
    fn build(&self) -> Element {
        self.element.clone()
    }

    fn __repr__(&self) -> String {
        format!("ElementBuilder({})", self.element.__repr__())
    }
}

// Convenience functions at module level
#[pyfunction]
pub fn div() -> ElementBuilder {
    ElementBuilder::div()
}

#[pyfunction]
pub fn text(content: String) -> ElementBuilder {
    ElementBuilder::text(content)
}

#[pyfunction]
pub fn button(label: String) -> ElementBuilder {
    ElementBuilder::button(label)
}

#[pyfunction]
pub fn input() -> ElementBuilder {
    ElementBuilder::input()
}
