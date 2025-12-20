"""Partial update example.

Demonstrates using id() and update_element() to update only specific
parts of the UI instead of replacing the entire root element.
"""

from wry_py import UiWindow, div, text, button

count = 0
window = UiWindow(title="Partial Update", width=400, height=300)


def make_counter():
    """Build just the counter display element."""
    return (
        text(f"Count: {count}")
        .id("counter")
        .text_size(48)
        .text_color("#fff")
        .build()
    )


def increment():
    global count
    count += 1
    # Only update the counter element, not the entire UI
    window.update_element("counter", make_counter())


def decrement():
    global count
    count -= 1
    window.update_element("counter", make_counter())


def reset():
    global count
    count = 0
    window.update_element("counter", make_counter())


def make_button(label, callback, color):
    return (
        button(label)
        .padding(12, 24)
        .bg(color)
        .text_color("#fff")
        .rounded(6)
        .cursor("pointer")
        .transition_colors(0.15)
        .hover_bg("#666")
        .on_click(callback)
    )


# Build the full UI once
root = (
    div()
    .size_full()
    .v_flex()
    .items_center()
    .justify_center()
    .gap(30)
    .bg("#1a1a1a")
    .child(make_counter())
    .child_builder(
        div()
        .h_flex()
        .gap(12)
        .child_builder(make_button("-", decrement, "#dc2626"))
        .child_builder(make_button("Reset", reset, "#525252"))
        .child_builder(make_button("+", increment, "#16a34a"))
    )
    .build()
)

window.set_root(root)
window.run()
