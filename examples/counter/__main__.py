from wry_py import UiWindow, div, text, button

class Counter:
    """Simple counter state container."""

    def __init__(self):
        self.count = 0
        self.window: UiWindow | None = None

    def set_window(self, window: UiWindow):
        self.window = window

    def increment(self):
        self.count += 1
        self.render()

    def decrement(self):
        self.count -= 1
        self.render()

    def render(self):
        """Update the UI with current state."""
        root = (
            div()
            .size_full()
            .v_flex()
            .items_center()
            .justify_center()
            .gap(10)
            .bg("#F8FAFC")
            .child_builder(
                text(f"Count: {self.count}")
                .text_size(48)
                .text_color("#0F172A")
                .text_weight("bold")
            )
            .child_builder(
                div()
                .h_flex()
                .gap(10)
                .child_builder(
                    button("Decrement")
                    .padding(10, 20)
                    .bg("#E2E8F0")
                    .text_color("#0F172A")
                    .on_click(self.decrement)
                )
                .child_builder(
                    button("Increment")
                    .padding(10, 20)
                    .bg("#0F172A")
                    .text_color("#E2E8F0")
                    .on_click(self.increment)
                )
            )
            .build()
        )
        
        if self.window:
            self.window.set_root(root)

def main():
    # Create window
    window = UiWindow(title="Counter", width=400, height=300, background_color="#FFFFFF")

    # Create counter state
    counter = Counter()
    counter.set_window(window)
    counter.render()

    # Run the event loop
    window.run()

if __name__ == "__main__":
    main()