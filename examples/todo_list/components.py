from typing import Callable
from wry_py import div, text, button, input


def header(title: str, on_add: Callable[[], None]):
    return (
        div()
        .h_flex()
        .justify_between()
        .items_center()
        .padding(20)
        .bg("#1e293b")
        .child_builder(
            text(title).text_size(24).text_weight("bold").text_color("#fff")
        )
        .child_builder(
            button("+ Add")
            .padding(10, 20)
            .bg("#3b82f6")
            .text_color("#fff")
            .rounded(6)
            .on_click(on_add)
        )
    )


def item_row(item: str, on_remove: Callable[[], None]):
    return (
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
            .on_click(on_remove)
        )
    )


def item_list(items: list[str], on_remove: Callable[[int], None]):
    container = div().v_flex().gap(8)

    if not items:
        return container.child_builder(empty_state())

    for i, item in enumerate(items):
        container = container.child_builder(
            item_row(item, lambda idx=i: on_remove(idx))
        )

    return container


def empty_state():
    return (
        div()
        .padding(40)
        .v_flex()
        .items_center()
        .child_builder(
            text("No items yet").text_color("#94a3b8").text_size(16)
        )
    )


def dialog(title: str, on_input: Callable[[str], None], on_cancel: Callable[[], None], on_confirm: Callable[[], None]):
    return (
        div()
        .absolute()
        .top(0)
        .left(0)
        .size_full()
        .bg("rgba(0,0,0,0.5)")
        .v_flex()
        .items_center()
        .justify_center()
        .child_builder(dialog_card(title, on_input, on_cancel, on_confirm))
    )


def dialog_card(title: str, on_input: Callable[[str], None], on_cancel: Callable[[], None], on_confirm: Callable[[], None]):
    return (
        div()
        .bg("#fff")
        .padding(24)
        .rounded(12)
        .v_flex()
        .gap(16)
        .width(320)
        .child_builder(
            text(title).text_size(20).text_weight("bold").text_color("#1e293b")
        )
        .child_builder(
            input()
            .placeholder("Enter item...")
            .padding(12)
            .bg("#f8fafc")
            .text_color("#1e293b")
            .border(1, "#e2e8f0")
            .rounded(6)
            .on_input(on_input)
        )
        .child_builder(dialog_buttons(on_cancel, on_confirm))
    )


def dialog_buttons(on_cancel: Callable[[], None], on_confirm: Callable[[], None]):
    return (
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
            .on_click(on_cancel)
        )
        .child_builder(
            button("Add")
            .padding(10, 20)
            .bg("#3b82f6")
            .text_color("#fff")
            .rounded(6)
            .on_click(on_confirm)
        )
    )
