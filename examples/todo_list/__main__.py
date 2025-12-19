from wry_py import UiWindow

from .app import TodoApp


def main():
    window = UiWindow(
        title="Todo List",
        width=480,
        height=600,
        background_color="#f1f5f9",
    )
    app = TodoApp()
    app.set_window(window)
    app.render()
    window.run()


if __name__ == "__main__":
    main()
