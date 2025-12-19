from dataclasses import dataclass
from wry_py import UiWindow, div, text, button


@dataclass
class Counter:
    # Current counter value
    count: int = 0

    # Window reference is injected after creation
    window: UiWindow | None = None

    def set_window(self, window: UiWindow):
        # Store the window so we can update its root later
        self.window = window

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

    # Initialize counter state and attach the window
    counter = Counter()
    counter.set_window(window)

    # Render the initial UI
    counter.render()

    # Start the event loop
    window.run()


if __name__ == "__main__":
    main()
