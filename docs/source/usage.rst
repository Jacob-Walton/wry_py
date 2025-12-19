Usage
=====

Layouts
-------

Vertical:

.. code-block:: python

   div().v_flex().gap(10).child_builder(text("A")).child_builder(text("B"))

Horizontal:

.. code-block:: python

   div().h_flex().gap(10).child_builder(button("Save")).child_builder(button("Cancel"))

Centered:

.. code-block:: python

   div().size_full().v_flex().items_center().justify_center()

Space between:

.. code-block:: python

   div().h_flex().justify_between()

Styling
-------

.. code-block:: python

   div()
   .bg("#2d3748")
   .text_color("#e2e8f0")
   .padding(20)
   .rounded(12)
   .border(2, "#3182ce")

Example: per-side margins, borders and per-corner radii

.. code-block:: python

    div()
    .mt(8)
    .mr(12)
    .mb(8)
    .ml(12)
    .border_top(2, "#e53e3e")
    .border_bottom(2, "#38a169")
    .rounded_tl(16)
    .rounded_br(8)

Hover and Transitions
---------------------

Buttons with hover:

.. code-block:: python

   button("Click me")
   .bg("#fafafa")
   .hover_bg("#d4d4d4")
   .text_color("#0a0a0a")
   .rounded(8)
   .transition_all(0.2)

Input with focus:

.. code-block:: python

   input()
   .bg("#171717")
   .border(1, "#404040")
   .focus_border_color("#a3a3a3")
   .transition_colors(0.15)

Image with hover scale:

.. code-block:: python

   image("photo.jpg")
   .width(120)
   .height(120)
   .object_fit("cover")
   .cursor("pointer")
   .transition_transform(0.3)
   .hover_scale(1.05)

Partial Updates
---------------

Instead of replacing the entire UI with ``set_root()``, you can update
individual elements using ``id()`` and ``update_element()``:

.. code-block:: python

   from wry_py import UiWindow, div, text, button

   count = 0
   window = UiWindow(title="Counter", width=400, height=300)

   def make_counter():
       return text(f"Count: {count}").id("counter").text_size(32).build()

   def increment():
       global count
       count += 1
       window.update_element("counter", make_counter())

   root = (
       div()
       .size_full()
       .v_flex()
       .items_center()
       .justify_center()
       .gap(20)
       .child(make_counter())
       .child_builder(button("+").on_click(increment))
       .build()
   )

   window.set_root(root)
   window.run()

This is more efficient when only a small part of the UI changes.

Local images
------------

For environments where `file://` access is restricted by the webview, use
`AssetCatalog` to register asset bytes and reference them by name. The
renderer will prefer the registered asset (embedded as a data URI) which
avoids local-file permission issues.

Example (register and use an asset):

.. code-block:: python

   from wry_py import AssetCatalog, image

   catalog = AssetCatalog()
   with open("examples/local_image/assets/logo.png", "rb") as f:
       catalog.add("logo.png", f.read())

   image("asset:logo.png").width(120).height(120).object_fit("cover")

Images
------

.. code-block:: python

   from wry_py import image

   image("https://example.com/photo.jpg")
   .width(200)
   .height(150)
   .object_fit("cover")
   .alt("Description")
   .rounded(8)

Text Input
----------

.. code-block:: python

   from wry_py import input

   current_value = ""

   def on_input(value: str):
       global current_value
       current_value = value

   field = (
       input()
       .placeholder("Enter text...")
       .padding(8, 12)
       .border(1, "#ccc")
       .on_input(on_input)
   )

Form Example
------------

.. code-block:: python

   from wry_py import UiWindow, div, text, input, button

   name = ""

   def on_name_input(value):
       global name
       name = value

   def on_submit():
       print(f"Submitted: {name}")

   root = (
       div()
       .v_flex()
       .gap(12)
       .padding(20)
       .child_builder(text("Name:"))
       .child_builder(
           input()
           .placeholder("Enter name")
           .padding(8, 12)
           .border(1, "#ccc")
           .on_input(on_name_input)
       )
       .child_builder(
           button("Submit")
           .padding(10, 20)
           .bg("#48bb78")
           .text_color("#fff")
           .on_click(on_submit)
       )
       .build()
   )

Todo List Example
-----------------

.. code-block:: python
    
   from wry_py import AppBase, UiWindow, div, text, button

   class TodoApp(AppBase):
       def __init__(self):
           super().__init__()
           self.items: list[str] = []

       def add_item(self):
           self.items.append(f"Item {len(self.items) + 1}")
           self.render()

       def remove_item(self, index: int):
           if 0 <= index < len(self.items):
               del self.items[index]
               self.render()

       def render(self):
           item_list = div().v_flex().gap(4)
           if not self.items:
               item_list = item_list.child_builder(
                   text("No items yet").text_color("#94a3b8").text_size(16)
               )
           for i, item in enumerate(self.items):
               item_list = item_list.child_builder(
                   div()
                   .h_flex()
                   .justify_between()
                   .items_center()
                   .padding(8)
                   .bg("#f8fafc")
                   .child_builder(text(item).text_color("#1e293b"))
                   .child_builder(
                       button("Remove")
                       .padding(6, 12)
                       .bg("#ef4444")
                       .text_color("#fff")
                       .rounded(4)
                       .on_click(lambda idx=i: self.remove_item(idx))
                   )
               )

           root = (
               div()
               .size_full()
               .v_flex()
               .padding(20)
               .gap(16)
               .child_builder(text("Todo List").text_size(24).text_weight("bold"))
               .child_builder(
                   button("Add Item")
                   .padding(10, 16)
                   .bg("#4299e1")
                   .text_color("#fff")
                   .on_click(self.add_item)
               )
               .child_builder(item_list)
               .build()
           )
           if self.window:
               self.window.set_root(root)

   window = UiWindow(title="Todo", width=400, height=500)
   app = TodoApp()
   app.set_window(window)
   app.run()
