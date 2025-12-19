from wry_py import AppBase, div

from .components import header, item_list, dialog


class TodoApp(AppBase):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[str] = []
        self.show_add_dialog: bool = False
        self.new_item_text: str = ""

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
        self.close_dialog()

    def remove_item(self, index: int):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.render()

    def render(self):
        root = (
            div()
            .size_full()
            .v_flex()
            .bg("#f1f5f9")
            .relative()
            .child_builder(header("Todo List", self.open_add_dialog))
            .child_builder(
                div()
                .v_flex()
                .padding(20)
                .gap(8)
                .child_builder(item_list(self.items, self.remove_item))
            )
        )

        if self.show_add_dialog:
            root = root.child_builder(
                dialog(
                    "Add New Item",
                    self.set_new_item_text,
                    self.close_dialog,
                    self.add_item,
                )
            )

        if self.window:
            self.window.set_root(root.build())
