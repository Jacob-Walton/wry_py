Concepts
========

Architecture
------------

Wry Py wraps Rust libraries via PyO3:

- **Wry** - Cross-platform webview
- **Tao** - Window and event handling

Elements are serialized to HTML/CSS and rendered in the native webview.

Builders and Elements
---------------------

``ElementBuilder`` is mutable and supports method chaining. Call ``.build()`` to get an immutable ``Element``.

.. code-block:: python

   # ElementBuilder
   builder = div().size_full().bg("#fff")

   # Element
   element = builder.build()

Use ``.child_builder()`` to add children without manually calling ``.build()``:

.. code-block:: python

   div().child_builder(text("Hello"))  # calls .build() internally

Element Types
-------------

- ``div()`` - Container
- ``text(content)`` - Text display
- ``button(label)`` - Button with click handler
- ``input()`` - Text input with input handler
- ``image(src)`` - Image

Styling States
--------------

Elements support hover and focus styles:

.. code-block:: python

   button("Submit")
   .bg("#fafafa")
   .hover_bg("#d4d4d4")
   .transition_all(0.2)

   input()
   .border(1, "#404040")
   .focus_border_color("#a3a3a3")

Available transitions:

- ``transition_all(seconds)`` - all properties
- ``transition_colors(seconds)`` - background, text, border colors
- ``transition_transform(seconds)`` - scale, etc.

Event Handling
--------------

Click:

.. code-block:: python

   def on_click():
       print("clicked")

   button("Click").on_click(on_click)

Input:

.. code-block:: python

   def on_input(value: str):
       print(value)

   input().on_input(on_input)

Mouse events:

.. code-block:: python

   div()
   .on_mouse_enter(on_enter)
   .on_mouse_leave(on_leave)

Callbacks run synchronously in the event loop.

Updating UI
-----------

Rebuild and call ``set_root()``:

.. code-block:: python

   def render():
       root = div().child_builder(text(f"Value: {state}")).build()
       window.set_root(root)

The Event Loop
--------------

``window.run()`` blocks until the window closes. Use ``window.close()`` to exit programmatically.

.. code-block:: python

   def quit():
       window.close()

   button("Quit").on_click(quit)

Platform Backends
-----------------

- **Windows** - WebView2 (Edge)
- **macOS** - WebKit (Safari)
- **Linux** - WebKitGTK (requires GTK libraries)
