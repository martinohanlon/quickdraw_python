quickdraw
=========

quickdraw is an API for using the Google Quick, Draw! Data. `quickdraw.withgoogle.com/data <https://quickdraw.withgoogle.com/data>`_

Getting started
---------------

+ Windows::

    pip install quickdraw

+ macOS::

    pip3 install quickdraw

+ Linux / Raspberry Pi::

    sudo pip3 install quickdraw

Use
---

.. code-block:: python

    from quickdraw import QuickDrawData
    qd = QuickDrawData()
    anvil_drawing = qd.get_drawing("anvil")
    
    print(anvil_drawing)
    print(anvil_drawing.strokes)

Documentation
-------------

to come.

