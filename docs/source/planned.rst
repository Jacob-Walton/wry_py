

Planned Features
================

Partial Updates
---------------

Support updating only parts of the UI tree instead of replacing the full root element on every render. This will improve performance and enable smoother UI transitions.

Transitions & Animations
-----------------------

Improve support for CSS transitions and add animation utilities (e.g., keyframes, fade, slide). Ensure transitions work reliably across platforms.

Raw CSS Styles
--------------

Add a ``.style()`` method to allow passing raw CSS styles directly to elements for advanced customization.

Element IDs & Classes
---------------------

Allow assigning IDs and classes to elements, enabling easier targeting from Python and event handlers without lambdas.

Advanced Event Targeting
------------------------

Provide a way to target elements in event handlers without relying on lambdas, making event handling more flexible.

Form Elements
-------------

Add support for dropdowns, radio buttons, checkboxes, and other common form controls.

Flexbox Utilities
-----------------

Expand flexbox support with utilities like ``gap``, ``wrap``, and ``basis`` for more complex layouts.

Tooltips
--------

Add tooltip support for elements, allowing display of additional information on hover or focus.

Size Constraints
----------------

Add ``.max_width()``, ``.min_width()``, ``.max_height()``, and ``.min_height()`` methods. Also add ``.full_width()`` and ``.full_height()`` for convenience.

Media Queries
-------------

Enable media queries or responsive style utilities for adapting layouts to different screen sizes (e.g., mobile vs desktop).

CSS Grid Layout
---------------

Add support for CSS grid layouts for advanced two-dimensional arrangements.

Animations
----------

Provide a way to define and trigger animations (e.g., keyframes, transitions on state change).

Drag-and-Drop
-------------

Add drag-and-drop support for elements, enabling interactive rearrangement and data transfer.

.. note::
	If you have any suggestions, feel free to open an issue on GitHub!
