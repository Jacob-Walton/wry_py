from wry_py import AppBase, UiWindow, div, text, button


class Counter(AppBase):
    def __init__(self) -> None:
        super().__init__()
        # Current counter value
        self.count: int = 0

    def increment(self):
        # Increase the counter and refresh the UI
        self.count += 1
        self.render()

    def decrement(self):
        # Decrease the counter and refresh the UI
        self.count -= 1
        self.render()

    def render(self):
        # Build the UI tree for the current state
        root = (
            div()  # Root container
            .size_full()
            .v_flex()
            .items_center()
            .justify_center()
            .gap(10)
            .bg("#F8FAFC")
            .child_builder(
                # Display the current count
                text(f"Count: {self.count}")
                .text_size(48)
                .text_color("#0F172A")
                .text_weight("bold")
            )
            .child_builder(
                # Button row
                div()
                .h_flex()
                .gap(10)
                .child_builder(
                    # Decrement button
                    button("Decrement")
                    .padding(10, 20)
                    .bg("#E2E8F0")
                    .text_color("#0F172A")
                    .on_click(self.decrement)
                )
                .child_builder(
                    # Increment button
                    button("Increment")
                    .padding(10, 20)
                    .bg("#0F172A")
                    .text_color("#E2E8F0")
                    .on_click(self.increment)
                )
            )
            .build()
        )

        # Only update the window if it has been attached
        if self.window:
            self.window.set_root(root)


def main():
    # Create the application window
    window = UiWindow(
        title="Counter",
        width=400,
        height=300,
        background_color="#FFFFFF",
    )

    # Initialize counter state, attach the window and run the app
    counter = Counter()
    counter.set_window(window)
    counter.run()


if __name__ == "__main__":
    main()
