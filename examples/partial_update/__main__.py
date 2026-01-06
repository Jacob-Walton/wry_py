"""Partial update demo.

Uses update_element() to update specific elements by ID.
Counter color transitions smoothly via DOM patching.
"""

from typing import Callable
from wry_py import UiWindow, div, text, button

count = 0
window = UiWindow(title="Partial Update", width=400, height=300)


def get_counter_color():
    """Return color based on count value."""
    if count > 0:
        return "#4ade80"  # green
    elif count < 0:
        return "#f87171"  # red
    return "#ffffff"  # white


def make_counter():
    """Build just the counter display element."""
    return (
        text(f"Count: {count}")
        .id("counter")
        .text_size(48)
        .text_color(get_counter_color())
        .transition_colors(0.3)
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



def make_button(label: str, callback: Callable[[], None], color: str):
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
