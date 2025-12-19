Wry Py
======

Python bindings for Wry and Tao, for building desktop applications with webviews.

.. code-block:: python

   from wry_py import UiWindow, div, text

   window = UiWindow(title="Hello World", width=400, height=300)

   root = (
       div()
       .size_full()
       .v_flex()
       .items_center()
       .justify_center()
       .child_builder(text("Hello, World!").text_size(32))
       .build()
   )

   window.set_root(root)
   window.run()

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Guide

   usage
   concepts

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api
