from __future__ import annotations

from pathlib import Path

from wry_py import UiWindow, div, image, text, AssetCatalog


def main() -> None:
    example_dir = Path(__file__).parent
    asset_path = example_dir / "assets" / "logo.png"

    window = UiWindow(title="Local Image Example", width=640, height=480)

    if asset_path.exists():
        # Register the image bytes in the AssetCatalog to avoid file:// restrictions
        catalog = AssetCatalog()
        with open(asset_path, "rb") as f:
            data = f.read()
        catalog.add("logo.png", data)

        # Refer to the registered asset by the asset: prefix
        root = (
            div()
            .size_full()
            .v_flex()
            .items_center()
            .justify_center()
            .child_builder(image("asset:logo.png").width(400).height(400).object_fit("contain"))
            .build()
        )
    else:
        root = (
            div()
            .size_full()
            .v_flex()
            .items_center()
            .justify_center()
            .child_builder(
                text(
                    "No image found. Place your image at examples/local_image/assets/logo.png and rerun."
                ).text_size(14)
            )
            .build()
        )

    window.set_root(root)
    window.run()


if __name__ == "__main__":
    main()
