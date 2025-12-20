from wry_py.app import AppBase
import wry_py


def test_appbase_run_calls_render_and_runs_window():
    rendered = {"called": False}

    class DummyApp(AppBase):
        def render(self):
            rendered["called"] = True
            assert self.window is not None
            self.window.set_root(wry_py.text("root").build())

    class FakeWindow:
        def __init__(self):
            self.root = None

        def set_root(self, root):
            self.root = root

        def run(self):
            # simulate event loop returning immediately
            return None

    app = DummyApp()
    w = FakeWindow()
    app.set_window(w) # type: ignore
    app.run()

    assert rendered["called"] is True
    # The window should have received an Element instance; verify type and content
    assert isinstance(w.root, wry_py.Element)
    assert "root" in w.root.to_json()
