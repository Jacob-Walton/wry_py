"""
Example demonstrating hover/focus styles, transitions, and images.
"""

from wry_py import UiWindow, div, text, button, image, input


def main():
    window = UiWindow(
        title="Gallery Example",
        width=600,
        height=550,
        background_color="#0a0a0a",
    )

    root = (
        div()
        .size_full()
        .v_flex()
        .gap(24)
        .padding(24)
        .bg("#0a0a0a")
        .child_builder(
            text("Hover & Focus Demo")
            .text_size(28)
            .text_weight("bold")
            .text_color("#fafafa")
        )
        # Buttons with hover effects and transitions
        .child_builder(
            div()
            .v_flex()
            .gap(8)
            .child_builder(
                text("Buttons with smooth transitions")
                .text_color("#737373")
                .text_size(14)
            )
            .child_builder(
                div()
                .h_flex()
                .gap(12)
                .child_builder(
                    button("Primary")
                    .padding(12, 24)
                    .bg("#fafafa")
                    .hover_bg("#d4d4d4")
                    .text_color("#0a0a0a")
                    .rounded(8)
                    .transition_all(0.2)
                )
                .child_builder(
                    button("Secondary")
                    .padding(12, 24)
                    .bg("#262626")
                    .hover_bg("#404040")
                    .text_color("#fafafa")
                    .rounded(8)
                    .transition_all(0.2)
                )
                .child_builder(
                    button("Outline")
                    .padding(12, 24)
                    .bg("transparent")
                    .hover_bg("#262626")
                    .text_color("#a3a3a3")
                    .hover_text_color("#fafafa")
                    .border(1, "#404040")
                    .hover_border_color("#525252")
                    .rounded(8)
                    .transition_all(0.2)
                )
                .child_builder(
                    button("Ghost")
                    .padding(12, 24)
                    .bg("transparent")
                    .hover_bg("#171717")
                    .text_color("#737373")
                    .hover_text_color("#e5e5e5")
                    .rounded(8)
                    .transition_colors(0.15)
                )
            )
        )
        # Input with focus styles
        .child_builder(
            div()
            .v_flex()
            .gap(8)
            .child_builder(
                text("Input with focus transition")
                .text_color("#737373")
                .text_size(14)
            )
            .child_builder(
                input()
                .placeholder("Focus me...")
                .padding(12)
                .bg("#171717")
                .text_color("#fafafa")
                .border(1, "#404040")
                .focus_border_color("#a3a3a3")
                .focus_bg("#0a0a0a")
                .rounded(8)
                .width(300)
                .transition_all(0.2)
            )
        )
        # Images with hover scale and opacity
        .child_builder(
            div()
            .v_flex()
            .gap(8)
            .child_builder(
                text("Images with hover effects")
                .text_color("#737373")
                .text_size(14)
            )
            .child_builder(
                div()
                .h_flex()
                .gap(16)
                .child_builder(
                    image("https://picsum.photos/120/120?random=1&grayscale")
                    .width(120)
                    .height(120)
                    .object_fit("cover")
                    .rounded(12)
                    .alt("Image 1")
                    .cursor("pointer")
                    .transition_transform(0.3)
                    .hover_scale(1.05)
                )
                .child_builder(
                    image("https://picsum.photos/120/120?random=2&grayscale")
                    .width(120)
                    .height(120)
                    .object_fit("cover")
                    .rounded(12)
                    .alt("Image 2")
                    .opacity(0.6)
                    .cursor("pointer")
                    .transition_all(0.3)
                    .hover_opacity(1.0)
                )
                .child_builder(
                    image("https://picsum.photos/120/120?random=3&grayscale")
                    .width(120)
                    .height(120)
                    .object_fit("cover")
                    .rounded(12)
                    .alt("Image 3")
                    .cursor("pointer")
                    .transition_all(0.3)
                    .hover_scale(1.05)
                    .hover_opacity(0.8)
                )
            )
        )
        # Card with hover
        .child_builder(
            div()
            .v_flex()
            .gap(8)
            .child_builder(
                text("Card with hover transition")
                .text_color("#737373")
                .text_size(14)
            )
            .child_builder(
                div()
                .padding(20)
                .bg("#171717")
                .hover_bg("#262626")
                .rounded(12)
                .border(1, "#262626")
                .hover_border_color("#404040")
                .v_flex()
                .gap(8)
                .cursor("pointer")
                .transition_all(0.2)
                .child_builder(
                    text("Hover over me")
                    .text_size(18)
                    .text_weight("bold")
                    .text_color("#fafafa")
                )
                .child_builder(
                    text("Smooth background transition on hover")
                    .text_color("#737373")
                )
            )
        )
        .build()
    )

    window.set_root(root)
    window.run()


if __name__ == "__main__":
    main()
