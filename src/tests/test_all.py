import wry_py


def test_module_exports():
    # Checks that the extension exposes expected symbols
    assert hasattr(wry_py, "AssetCatalog")
    assert hasattr(wry_py, "ElementBuilder")
    assert hasattr(wry_py, "UiWindow")
    assert hasattr(wry_py, "div")
    assert hasattr(wry_py, "text")


def test_asset_catalog_smoke():
    catalog = wry_py.AssetCatalog()
    png_bytes = b"\x89PNG\r\n\x1a\n"
    catalog.add("logo.png", png_bytes)
    uri = catalog.get_data_uri("logo.png")
    assert uri is not None
    assert uri.startswith("data:image/png;base64,")
