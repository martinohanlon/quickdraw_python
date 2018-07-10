quickdraw
=========

`Google Quick, Draw! <https://quickdraw.withgoogle.com/>`_ is a game which is training a neural network to recognise doodles.

`quickdraw` is an API for using the Google Quick, Draw! data `quickdraw.withgoogle.com/data <https://quickdraw.withgoogle.com/data>`_, downloading the data files as and when needed, caching them locally and allowing them to be used.

Getting started
---------------

+ Windows 

.. code-block:: bash

    pip install quickdraw

+ macOS 

.. code-block:: bash

    pip3 install quickdraw

+ Linux / Raspberry Pi 

.. code-block:: bash

    sudo pip3 install quickdraw

Use
---

Open the Quick Draw data and pull back an **anvil** drawing.

.. code-block:: python

    from quickdraw import QuickDrawData
    qd = QuickDrawData()
    anvil = qd.get_drawing("anvil")
    
    print(anvil)
    
`quickdraw` will download the anvil data file and return a random drawing of an "anvil" (well a doodle of an anvil anyway).

Drawings are returned as `QuickDrawing` objects which exposes the properties of the drawing.

.. code-block:: python

    print(anvil.name)
    print(anvil.key_id)
    print(anvil.countrycode)
    print(anvil.recognized)
    print(anvil.timestamp)
    print(anvil.no_of_strokes)
    print(anvil.image_data)
    print(anvil.strokes)

`strokes` is a list of pen strokes containing a list of (x,y) coordinates which make up the drawing.

Open a group of Quick Draw drawings using `QuickDrawDataGroup` passing the name of the drawing ("anvil", "aircraft", "baseball", etc).

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    anvils = QuickDrawDataGroup("anvil")
    print(anvils.drawing_count)
    print(anvils.get_drawing())

You can get a list of all the drawings using the `drawing_names` property of QuickDrawData.

.. code-block:: python

    from quickdraw import QuickDrawData

    qd = QuickDrawData()
    print(qd.drawing_names)

By default only 1000 drawings are opened, you can change this by modifying the `max_drawings` parameter of `QuickDrawDataGroup`, setting it to `None` will open all the drawings in that group.

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    anvils = QuickDrawDataGroup("anvil", max_drawings=None)
    print(anvils.drawing_count)

To iterate through all the drawings in a group use the `drawings` generator.

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    qdg = QuickDrawDataGroup("anvil")
    for drawing in qdg.drawings:
        print(drawing)

Documentation
-------------

to come.

Warning
-------

The drawings have been moderated but there is no guarantee it'll actually be a picture of what you are asking it for (although in my experience they are)!

Status
------

**Alpha** - under active dev, the API may change, problems might occur.