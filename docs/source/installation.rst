Installation
============

Requirements: Python 3.10+

.. code-block:: bash

   pip install wry_py

Linux Dependencies
------------------

Wry Py uses GTK and WebKitGTK on Linux. Install the required libraries:

**Debian/Ubuntu:**

.. code-block:: bash

   sudo apt install libgtk-3-dev libwebkit2gtk-4.1-dev

**Fedora:**

.. code-block:: bash

   sudo dnf install gtk3-devel webkit2gtk4.1-devel

**Arch Linux:**

.. code-block:: bash

   sudo pacman -S gtk3 webkit2gtk-4.1

macOS and Windows require no additional dependencies.

Building from Source
--------------------

Requires Rust 1.70+ and maturin:

.. code-block:: bash

   git clone https://github.com/Jacob-Walton/wry_py.git
   cd wry_py
   pip install maturin
   maturin develop --release
