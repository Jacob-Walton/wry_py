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

   from dataclasses import dataclass, field
   from wry_py import UiWindow, div, text, button

   @dataclass
   class TodoApp:
       items: list[str] = field(default_factory=list)
       window: UiWindow | None = None

       def set_window(self, window):
           self.window = window

       def add_item(self):
           self.items.append(f"Item {len(self.items) + 1}")
           self.render()

       def render(self):
           item_list = div().v_flex().gap(4)
           for item in self.items:
               item_list = item_list.child_builder(
                   text(item).padding(8).bg("#f7fafc")
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
   app.render()
   window.run()
