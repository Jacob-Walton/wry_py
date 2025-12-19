from dataclasses import dataclass, field
from wry_py import UiWindow, div, text, button, input


@dataclass
class TodoApp:
    items: list[str] = field(default_factory=list)
    window: UiWindow | None = None
    show_add_dialog: bool = False
    new_item_text: str = ""

    def set_window(self, window: UiWindow):
        self.window = window

    def open_add_dialog(self):
        self.show_add_dialog = True
        self.new_item_text = ""
        self.render()

    def close_dialog(self):
        self.show_add_dialog = False
        self.new_item_text = ""
        self.render()

    def set_new_item_text(self, value: str):
        self.new_item_text = value

    def add_item(self):
        if self.new_item_text.strip():
            self.items.append(self.new_item_text.strip())
        self.show_add_dialog = False
        self.new_item_text = ""
        self.render()

    def remove_item(self, index: int):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.render()

    def render(self):
        # Item list
        item_list = div().v_flex().gap(8)
        for i, item in enumerate(self.items):
            idx = i  # capture for closure
            item_list = item_list.child_builder(
                div()
                .h_flex()
                .justify_between()
                .items_center()
                .padding(12)
                .bg("#f8fafc")
                .rounded(6)
                .child_builder(text(item).text_color("#1e293b"))
                .child_builder(
                    button("Remove")
                    .padding(6, 12)
                    .bg("#ef4444")
                    .text_color("#fff")
                    .rounded(4)
                    .on_click(lambda idx=idx: self.remove_item(idx))
                )
            )

        # Empty state
        if not self.items:
            item_list = item_list.child_builder(
                div()
                .padding(40)
                .v_flex()
                .items_center()
                .child_builder(
                    text("No items yet").text_color("#94a3b8").text_size(16)
                )
            )

        # Main layout
        root = (
            div()
            .size_full()
            .v_flex()
            .bg("#f1f5f9")
            .relative()
            .child_builder(
                # Header
                div()
                .h_flex()
                .justify_between()
                .items_center()
                .padding(20)
                .bg("#1e293b")
                .child_builder(
                    text("Todo List").text_size(24).text_weight("bold").text_color("#fff")
                )
                .child_builder(
                    button("+ Add")
                    .padding(10, 20)
                    .bg("#3b82f6")
                    .text_color("#fff")
                    .rounded(6)
                    .on_click(self.open_add_dialog)
                )
            )
            .child_builder(
                # Content area
                div()
                .v_flex()
                .padding(20)
                .gap(8)
                .child_builder(item_list)
            )
        )

        # Add dialog overlay
        if self.show_add_dialog:
            root = root.child_builder(
                div()
                .absolute()
                .top(0)
                .left(0)
                .size_full()
                .bg("rgba(0,0,0,0.5)")
                .v_flex()
                .items_center()
                .justify_center()
                .child_builder(
                    div()
                    .bg("#fff")
                    .padding(24)
                    .rounded(12)
                    .v_flex()
                    .gap(16)
                    .width(320)
                    .child_builder(
                        text("Add New Item")
                        .text_size(20)
                        .text_weight("bold")
                        .text_color("#1e293b")
                    )
                    .child_builder(
                        input()
                        .placeholder("Enter item...")
                        .padding(12)
                        .bg("#f8fafc")
                        .text_color("#1e293b")
                        .border(1, "#e2e8f0")
                        .rounded(6)
                        .on_input(self.set_new_item_text)
                    )
                    .child_builder(
                        div()
                        .h_flex()
                        .gap(12)
                        .justify_between()
                        .child_builder(
                            button("Cancel")
                            .padding(10, 20)
                            .bg("#e2e8f0")
                            .text_color("#1e293b")
                            .rounded(6)
                            .on_click(self.close_dialog)
                        )
                        .child_builder(
                            button("Add")
                            .padding(10, 20)
                            .bg("#3b82f6")
                            .text_color("#fff")
                            .rounded(6)
                            .on_click(self.add_item)
                        )
                    )
                )
            )

        if self.window:
            self.window.set_root(root.build())


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
