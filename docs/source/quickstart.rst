Quickstart
==========

Creating a Window
-----------------

.. code-block:: python

   from wry_py import UiWindow

   window = UiWindow(
       title="My App",
       width=800,
       height=600,
       background_color="#1a1a1a"
   )
   window.run()

Adding Content
--------------

Content is built using chained method calls. Each method returns ``self``, and ``.build()`` produces the final element.

.. code-block:: python

   from wry_py import UiWindow, div, text

   window = UiWindow(title="Hello World")

   root = (
       div()
       .size_full()
       .v_flex()
       .items_center()
       .justify_center()
       .bg("#f0f0f0")
       .child_builder(
           text("Hello, World!")
           .text_size(32)
           .text_color("#333")
       )
       .build()
   )

   window.set_root(root)
   window.run()

Handling Clicks
---------------

.. code-block:: python

   from wry_py import UiWindow, div, button

   def on_click():
       print("Clicked")

   window = UiWindow(title="Button Example")

   root = (
       div()
       .size_full()
       .v_flex()
       .items_center()
       .justify_center()
       .child_builder(
           button("Click Me")
           .padding(15, 30)
           .bg("#007bff")
           .text_color("#fff")
           .on_click(on_click)
       )
       .build()
   )

   window.set_root(root)
   window.run()

Updating the UI
---------------

Rebuild the element tree and call ``set_root()`` again:

.. code-block:: python

   from wry_py import UiWindow, div, text, button

   count = 0
   window = None

   def increment():
       global count
       count += 1
       render()

   def render():
       root = (
           div()
           .size_full()
           .v_flex()
           .items_center()
           .justify_center()
           .gap(20)
           .child_builder(text(f"Count: {count}").text_size(48))
           .child_builder(
               button("Increment")
               .padding(12, 24)
               .bg("#28a745")
               .text_color("#fff")
               .on_click(increment)
           )
           .build()
       )
       window.set_root(root)

   window = UiWindow(title="Counter", width=400, height=300)
   render()
   window.run()

Using Classes
-------------

For larger applications, encapsulate state in a class:

.. code-block:: python

   from dataclasses import dataclass
   from wry_py import UiWindow, div, text, button

   @dataclass
   class Counter:
       count: int = 0
       window: UiWindow | None = None

       def set_window(self, window: UiWindow):
           self.window = window

       def increment(self):
           self.count += 1
           self.render()

       def decrement(self):
           self.count -= 1
           self.render()

       def render(self):
           root = (
               div()
               .size_full()
               .v_flex()
               .items_center()
               .justify_center()
               .gap(10)
               .bg("#F8FAFC")
               .child_builder(
                   text(f"Count: {self.count}")
                   .text_size(48)
                   .text_weight("bold")
               )
               .child_builder(
                   div()
                   .h_flex()
                   .gap(10)
                   .child_builder(
                       button("-").padding(10, 20).bg("#E2E8F0").on_click(self.decrement)
                   )
                   .child_builder(
                       button("+").padding(10, 20).bg("#0F172A").text_color("#fff").on_click(self.increment)
                   )
               )
               .build()
           )
           if self.window:
               self.window.set_root(root)

   window = UiWindow(title="Counter", width=400, height=300)
   counter = Counter()
   counter.set_window(window)
   counter.render()
   window.run()
