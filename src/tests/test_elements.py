import json
try:
    import wry_py
except ImportError:
    print("wry_py module not found. Ensure it is installed and accessible.")


def test_text_and_button_elements():
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
    catalog = wry_py.AssetCatalog()
    # Add asset with a path-like name; lookup by basename should work
    catalog.add("images/logo.png", b"\x89PNG\r\n\x1a\n")
    uri = catalog.get_data_uri("logo.png")
    assert uri is not None
    assert uri.startswith("data:image/png;base64,")


def test_div_element():
    el = wry_py.div().build()
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "div"


def test_input_element():
    el = wry_py.input().placeholder("Enter text").value("test").build()
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "input"
    assert parsed.get("placeholder") == "Enter text"
    assert parsed.get("value") == "test"


def test_image_element():
    el = wry_py.image("test.png").alt("Test image").object_fit("cover").build()
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "image"
    assert parsed.get("text_content") == "test.png"
    assert parsed.get("alt") == "Test image"
    assert parsed.get("object_fit") == "cover"


def test_checkbox_element():
    el = wry_py.checkbox("Accept terms").checked(True).build()
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "checkbox"
    assert parsed.get("label") == "Accept terms"
    assert parsed.get("checked") is True


def test_radio_element():
    el = wry_py.radio("Option A").group("options").value("a").checked(True).build()
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "radio"
    assert parsed.get("label") == "Option A"
    assert parsed.get("radio_group") == "options"
    assert parsed.get("value") == "a"
    assert parsed.get("checked") is True


def test_select_element():
    el = (
        wry_py.select()
        .option("a", "Option A")
        .option("b", "Option B")
        .selected("b")
        .build()
    )
    parsed = json.loads(el.to_json())
    assert parsed.get("element_type") == "select"
    assert len(parsed.get("options", [])) == 2
    assert parsed.get("selected") == "b"


class TestLayoutMethods:
    def test_size_methods(self):
        el = wry_py.div().width(100).height(200).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("width") == 100
        assert parsed.get("height") == 200

    def test_size_full(self):
        el = wry_py.div().size_full().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("size_full") is True

    def test_min_max_size(self):
        el = wry_py.div().min_width(50).max_width(500).min_height(100).max_height(800).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("min_width") == 50
        assert parsed.get("max_width") == 500
        assert parsed.get("min_height") == 100
        assert parsed.get("max_height") == 800

    def test_flex_layout(self):
        el = wry_py.div().v_flex().items_center().justify_center().gap(10).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("flex_direction") == "column"
        assert parsed.get("align_items") == "center"
        assert parsed.get("justify_content") == "center"
        assert parsed.get("gap") == 10

    def test_h_flex(self):
        el = wry_py.div().h_flex().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("flex_direction") == "row"

    def test_flex_utilities(self):
        el = wry_py.div().flex_wrap().flex_grow(2).flex_shrink(0).flex_basis("100px").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("flex_wrap") == "wrap"
        assert parsed.get("flex_grow") == 2
        assert parsed.get("flex_shrink") == 0
        assert parsed.get("flex_basis") == "100px"

    def test_flex_1(self):
        el = wry_py.div().flex_1().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("flex_grow") == 1
        assert parsed.get("flex_shrink") == 1
        assert parsed.get("flex_basis") == "0%"

    def test_grid_layout(self):
        el = wry_py.div().grid_cols("1fr 1fr 1fr").grid_rows("auto 1fr").gap(16).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("display_grid") is True
        assert parsed.get("grid_template_columns") == "1fr 1fr 1fr"
        assert parsed.get("grid_template_rows") == "auto 1fr"
        assert parsed.get("gap") == 16

    def test_grid_item(self):
        el = wry_py.div().col("span 2").row("1 / 3").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("grid_column") == "span 2"
        assert parsed.get("grid_row") == "1 / 3"

    def test_place_items(self):
        el = wry_py.div().grid().place_center().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("display_grid") is True
        assert parsed.get("place_items") == "center"


class TestStylingMethods:
    def test_colors(self):
        el = wry_py.div().bg("#ff0000").text_color("#ffffff").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("background_color") == "#ff0000"
        assert parsed.get("text_color") == "#ffffff"

    def test_border(self):
        el = wry_py.div().border(2, "#000").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("border_width") == 2
        assert parsed.get("border_color") == "#000"

    def test_border_radius(self):
        el = wry_py.div().rounded(8).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("border_radius") == 8

    def test_per_corner_radius(self):
        el = wry_py.div().rounded_tl(4).rounded_tr(8).rounded_br(12).rounded_bl(16).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("border_radius_top_left") == 4
        assert parsed.get("border_radius_top_right") == 8
        assert parsed.get("border_radius_bottom_right") == 12
        assert parsed.get("border_radius_bottom_left") == 16

    def test_padding(self):
        el = wry_py.div().padding(10).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("padding") == 10

    def test_padding_xy(self):
        el = wry_py.div().padding(10, 20).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("padding_top") == 10
        assert parsed.get("padding_bottom") == 10
        assert parsed.get("padding_left") == 20
        assert parsed.get("padding_right") == 20

    def test_margin(self):
        el = wry_py.div().margin(15).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("margin") == 15

    def test_opacity(self):
        el = wry_py.div().opacity(0.5).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("opacity") == 0.5

    def test_cursor(self):
        el = wry_py.div().cursor("pointer").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("cursor") == "pointer"


class TestTransitions:
    def test_transition_all(self):
        el = wry_py.div().transition_all(0.3).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("transition") == "all 0.3s ease"

    def test_transition_colors(self):
        el = wry_py.div().transition_colors(0.2).build()
        parsed = json.loads(el.to_json())
        assert "background" in parsed.get("transition", "")
        assert "color" in parsed.get("transition", "")

    def test_transition_transform(self):
        el = wry_py.div().transition_transform(0.15).build()
        parsed = json.loads(el.to_json())
        assert "transform" in parsed.get("transition", "")


class TestHoverStyles:
    def test_hover_bg(self):
        el = wry_py.div().hover_bg("#ff0000").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("hover_bg") == "#ff0000"

    def test_hover_text_color(self):
        el = wry_py.div().hover_text_color("#00ff00").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("hover_text_color") == "#00ff00"

    def test_hover_scale(self):
        el = wry_py.div().hover_scale(1.1).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("hover_scale") == 1.1


class TestFocusStyles:
    def test_focus_border_color(self):
        el = wry_py.input().focus_border_color("#0000ff").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("focus_border_color") == "#0000ff"


class TestPositioning:
    def test_absolute(self):
        el = wry_py.div().absolute().top(10).left(20).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("position") == "absolute"
        assert parsed.get("top") == 10
        assert parsed.get("left") == 20

    def test_relative(self):
        el = wry_py.div().relative().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("position") == "relative"


class TestChildren:
    def test_child_builder(self):
        el = wry_py.div().child_builder(wry_py.text("Hello")).build()
        parsed = json.loads(el.to_json())
        assert len(parsed.get("children", [])) == 1
        assert parsed["children"][0].get("element_type") == "text"

    def test_child_text(self):
        el = wry_py.div().child_text("Direct text").build()
        parsed = json.loads(el.to_json())
        assert len(parsed.get("children", [])) == 1

    def test_multiple_children(self):
        el = (
            wry_py.div()
            .child_builder(wry_py.text("One"))
            .child_builder(wry_py.text("Two"))
            .child_builder(wry_py.text("Three"))
            .build()
        )
        parsed = json.loads(el.to_json())
        assert len(parsed.get("children", [])) == 3


class TestIdentification:
    def test_id(self):
        el = wry_py.div().id("my-element").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("user_id") == "my-element"

    def test_class_name(self):
        el = wry_py.div().class_name("container").build()
        parsed = json.loads(el.to_json())
        assert "container" in parsed.get("class_names", [])

    def test_classes(self):
        el = wry_py.div().classes(["one", "two", "three"]).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("class_names") == ["one", "two", "three"]


class TestText:
    def test_text_size(self):
        el = wry_py.text("Hello").text_size(24).build()
        parsed = json.loads(el.to_json())
        assert parsed.get("font_size") == 24

    def test_text_weight(self):
        el = wry_py.text("Hello").text_weight("bold").build()
        parsed = json.loads(el.to_json())
        assert parsed.get("font_weight") == "bold"

    def test_text_center(self):
        el = wry_py.text("Hello").text_center().build()
        parsed = json.loads(el.to_json())
        assert parsed.get("text_align") == "center"
