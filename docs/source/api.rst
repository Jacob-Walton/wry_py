API Reference
=============

Functions
---------

.. function:: div()

   Returns an ``ElementBuilder`` for a container element.

.. function:: text(content: str)

   Returns an ``ElementBuilder`` for text display.

.. function:: button(label: str)

   Returns an ``ElementBuilder`` for a button.

.. function:: input()

   Returns an ``ElementBuilder`` for a text input.

.. function:: image(src: str)

   Returns an ``ElementBuilder`` for an image.

UiWindow
--------

.. class:: UiWindow(title=None, width=None, height=None, background_color=None)

   :param title: Window title. Default: ``"Python App"``
   :param width: Width in pixels. Default: ``800``
   :param height: Height in pixels. Default: ``600``
   :param background_color: Hex color. Default: ``"#1a1a1a"``

   .. method:: set_root(element: Element)

      Set the root element and render it.

   .. method:: set_title(title: str)

      Change the window title.

   .. method:: run()

      Start the event loop. Blocks until the window closes.

   .. method:: close()

      Close the window and exit the event loop.

   .. method:: is_running() -> bool

      Returns ``True`` if the event loop is running.

AppBase
-------

.. class:: AppBase()

   Base class intended for application code. Subclass this in Python to
   encapsulate application state and rendering logic. Typical usage is to
   implement ``render()`` and call ``set_window()`` to attach a ``UiWindow``.

   .. method:: set_window(window: UiWindow)

      Attach a ``UiWindow`` instance to the app. The app can use
      ``window.set_root(...)`` to update the UI.

   .. method:: render()

      Build and set the root element for the window. Subclasses MUST
      implement this method and call ``self.window.set_root(...)`` with
      the constructed ``Element``.

   .. method:: run()

      Convenience: render once and start the window event loop. Raises
      ``RuntimeError`` if no window has been attached.

   .. method:: set_root(element: Element)

      Convenience wrapper to call ``window.set_root(element)``. Raises
      ``RuntimeError`` if no window is attached.

   .. method:: on_start()

      Optional lifecycle hook invoked before `run()` begins.

   .. method:: on_close()

      Optional lifecycle hook invoked after the window closes.

Element
-------

.. class:: Element(element_type=None)

   Immutable element. Created by calling ``.build()`` on an ``ElementBuilder``.

   .. method:: to_json() -> str

      Serialize to JSON.

ElementBuilder
--------------

All methods return ``self`` for chaining unless noted.

Factory Methods
^^^^^^^^^^^^^^^

.. classmethod:: ElementBuilder.div()
.. classmethod:: ElementBuilder.text(content: str)
.. classmethod:: ElementBuilder.button(label: str)
.. classmethod:: ElementBuilder.image(src: str)
.. classmethod:: ElementBuilder.input()

Size
^^^^

.. method:: width(w: float)
.. method:: height(h: float)
.. method:: size(w: float, h: float)
.. method:: size_full()

   Sets width and height to 100%.

Layout
^^^^^^

.. method:: v_flex()

   Vertical flex layout (column).

.. method:: h_flex()

   Horizontal flex layout (row).

.. method:: items_center()

   Center items on the cross axis.

.. method:: justify_center()

   Center items on the main axis.

.. method:: justify_between()

   Space between items.

.. method:: gap(g: float)

   Gap between children in pixels.

Padding
^^^^^^^

.. method:: padding(y: float, x: float = None)

   One arg: all sides. Two args: vertical, horizontal.

.. method:: p(y: float, x: float = None)

   Alias for ``padding()``.

.. method:: pt(p: float)
.. method:: pr(p: float)
.. method:: pb(p: float)
.. method:: pl(p: float)
.. method:: px(p: float)

   Left and right.

.. method:: py(p: float)

   Top and bottom.

.. method:: margin(m: float)
.. method:: m(m: float)

   Alias for ``margin()``.

Styling
^^^^^^^

.. method:: bg(color: str)

   Background color (hex or CSS).

.. method:: text_color(color: str)
.. method:: rounded(radius: float)

   Border radius in pixels.

.. method:: border(width: float, color: str)
.. method:: b(color: str)

   1px solid border.

.. method:: overflow_hidden()
.. method:: overflow(value: str)

Text
^^^^

.. method:: text_size(size: float)

   Font size in pixels.

.. method:: text_weight(weight: str)

   ``"normal"``, ``"bold"``, or ``"100"``-``"900"``.

.. method:: text_align(align: str)
.. method:: text_center()
.. method:: word_wrap(value: str)

Transitions
^^^^^^^^^^^

.. method:: transition_all(seconds: float)

   Transition all properties with the given duration.

.. method:: transition_colors(seconds: float)

   Transition background, text, and border colors.

.. method:: transition_transform(seconds: float)

   Transition transform (scale, etc.).

.. method:: transition(value: str)

   Raw CSS transition value for advanced use.

Effects
^^^^^^^

.. method:: opacity(value: float)

   Set opacity (0.0 to 1.0).

.. method:: cursor(value: str)

   Set cursor style (``"pointer"``, ``"grab"``, ``"not-allowed"``).

Hover Styles
^^^^^^^^^^^^

.. method:: hover_bg(color: str)
.. method:: hover_text_color(color: str)
.. method:: hover_border_color(color: str)
.. method:: hover_opacity(value: float)
.. method:: hover_scale(value: float)

   Scale on hover (e.g., ``1.05`` for 5% larger).

Focus Styles
^^^^^^^^^^^^

.. method:: focus_bg(color: str)
.. method:: focus_text_color(color: str)
.. method:: focus_border_color(color: str)

Position
^^^^^^^^

.. method:: position(value: str)

   ``"static"``, ``"relative"``, ``"absolute"``, ``"fixed"``.

.. method:: absolute()
.. method:: relative()
.. method:: top(value: float)
.. method:: right(value: float)
.. method:: bottom(value: float)
.. method:: left(value: float)

Children
^^^^^^^^

.. method:: child(child: Element)

   Add an ``Element`` as a child.

.. method:: child_builder(child: ElementBuilder)

   Add an ``ElementBuilder`` as a child. Calls ``.build()`` internally.

.. method:: child_text(text: str)

   Add text as a child.

Events
^^^^^^

.. method:: on_click(callback: Callable[[], None])

   Register a click handler.

.. method:: on_input(callback: Callable[[str], None])

   Register an input handler. Receives the current value.

.. method:: on_mouse_enter(callback: Callable[[], None])

   Register a handler for mouse enter.

.. method:: on_mouse_leave(callback: Callable[[], None])

   Register a handler for mouse leave.

.. method:: on_mouse_down(callback: Callable[[], None])

   Register a handler for mouse button press.

.. method:: on_mouse_up(callback: Callable[[], None])

   Register a handler for mouse button release.

Image
^^^^^

.. method:: alt(text: str)

   Set alt text for accessibility.

.. method:: object_fit(value: str)

   Set object-fit (``"cover"``, ``"contain"``, ``"fill"``).

Input
^^^^^

.. method:: value(val: str)

   Set the input value.

.. method:: placeholder(text: str)

   Set placeholder text.

Build
^^^^^

.. method:: build() -> Element

   Finalize and return the ``Element``.
