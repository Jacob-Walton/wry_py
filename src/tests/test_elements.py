import json


def test_text_and_button_elements():
    import wry_py

    # Create a text element and ensure its JSON is valid and identifies as text
    text_builder = wry_py.text("hello")
    text_el = text_builder.build()
    text_json = text_el.to_json()
    parsed = json.loads(text_json)
    assert parsed.get("element_type") == "text"

    # Create a button element and verify JSON
    btn_el = wry_py.button("Click me").build()
    btn_json = btn_el.to_json()
    parsed_btn = json.loads(btn_json)
    assert parsed_btn.get("element_type") == "button"


def test_asset_catalog_basename_lookup():
    import wry_py

    catalog = wry_py.AssetCatalog()
    # Add asset with a path-like name; lookup by basename should work
    catalog.add("images/logo.png", b"\x89PNG\r\n\x1a\n")
    uri = catalog.get_data_uri("logo.png")
    assert uri is not None
    assert uri.startswith("data:image/png;base64,")
