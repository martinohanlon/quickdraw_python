quickdraw
=========

|pypibadge| |docsbadge|

.. raw:: html

    <iframe allowtransparency="true" style="background-color: white;" src="https://github.com/sponsors/martinohanlon/button" title="Sponsor martinohanlon" height="35" width="116" style="border: 0;"></iframe>

`Quick Draw`_ is a drawing game which is training a neural network to recognise doodles.

|quickdraw|

``quickdraw`` is an API for accessing the `Quick Draw data`_ - it downloads the data files as and when needed, caches them locally and interprets them so they can be used.

|quickdrawpreview|

Created by `Martin O'Hanlon`_ (`@martinohanlon`_, `stuffaboutco.de`_).

Getting started
---------------

Install the `quickdraw` python library using `pip`.

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

Here are some examples of how to use ``quickdraw`` but be sure to also checkout the `API documentation`_ for more information.

Open the Quick Draw data using `QuickDrawData`_ and pull back a drawing of an **anvil**.

.. code-block:: python

    from quickdraw import QuickDrawData
    qd = QuickDrawData()
    anvil = qd.get_drawing("anvil")
    
    print(anvil)
    
``quickdraw`` will download the ``anvil.bin`` data file and return the data for a random drawing of an anvil (well a doodle of an anvil anyway).

Drawings are returned as `QuickDrawing`_ objects which exposes the properties of the drawing.

.. code-block:: python

    print(anvil.name)
    print(anvil.key_id)
    print(anvil.countrycode)
    print(anvil.recognized)
    print(anvil.timestamp)
    print(anvil.no_of_strokes)
    print(anvil.image_data)
    print(anvil.strokes)

You can save the drawing using the ``image`` property.

.. code-block:: python

    anvil.image.save("my_anvil.gif")

|myanvil|

You can open a group of Quick Draw drawings using `QuickDrawDataGroup`_ passing the name of the drawing ("anvil", "aircraft", "baseball", etc).

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    anvils = QuickDrawDataGroup("anvil")
    print(anvils.drawing_count)
    print(anvils.get_drawing())

By default only 1000 drawings are opened, you can change this by modifying the ``max_drawings`` parameter of `QuickDrawDataGroup`_, setting it to ``None`` will open all the drawings in that group.

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    anvils = QuickDrawDataGroup("anvil", max_drawings=None)
    print(anvils.drawing_count)

To iterate through all the drawings in a group use the `drawings`_ generator.

.. code-block:: python

    from quickdraw import QuickDrawDataGroup

    qdg = QuickDrawDataGroup("anvil")
    for drawing in qdg.drawings:
        print(drawing)

You can get a list of all the drawing names using the `drawing_names`_ property of `QuickDrawData`_.

.. code-block:: python

    from quickdraw import QuickDrawData

    qd = QuickDrawData()
    print(qd.drawing_names)

Examples
--------

`Code examples`_ can be found in the `quickdraw GitHub repository`_.

Documentation
-------------

`API documentation`_ can be found at `quickdraw.readthedocs.io`_

Warning
-------

The drawings have been moderated but there is no guarantee it'll actually be a picture of what you are asking it for (although in my experience they are)!

Status
------

**Stable**. 

Raise any `issues`_ in the `github repository`_.

.. |quickdraw| image:: https://raw.githubusercontent.com/martinohanlon/quickdraw_python/master/docs/images/quickdraw.png
   :scale: 100 %
   :alt: quickdraw

.. |quickdrawpreview| image:: https://raw.githubusercontent.com/martinohanlon/quickdraw_python/master/docs/images/quickdraw_preview.jpg
   :scale: 100 %
   :alt: quickdraw_preview

.. |myanvil| image:: https://raw.githubusercontent.com/martinohanlon/quickdraw_python/master/docs/images/my_anvil.gif
   :scale: 100 %
   :alt: quickdraw_preview

.. |pypibadge| image:: https://badge.fury.io/py/quickdraw.svg
   :target: https://badge.fury.io/py/quickdraw
   :alt: Latest Version

.. |docsbadge| image:: https://readthedocs.org/projects/quickdraw/badge/
   :target: https://readthedocs.org/projects/quickdraw/
   :alt: Docs

.. _Martin O'Hanlon: https://github.com/martinohanlon
.. _stuffaboutco.de: http://stuffaboutco.de
.. _@martinohanlon: https://twitter.com/martinohanlon
.. _API documentation: https://quickdraw.readthedocs.io/en/latest/api.html
.. _quickdraw.readthedocs.io: https://quickdraw.readthedocs.io
.. _Quick Draw: https://quickdraw.withgoogle.com/
.. _Quick Draw data: https://quickdraw.withgoogle.com/data
.. _Code examples: https://github.com/martinohanlon/quickdraw_python/tree/master/examples
.. _quickdraw GitHub repository: https://github.com/martinohanlon/quickdraw_python
.. _QuickDrawing: https://quickdraw.readthedocs.io/en/latest/api.html#quickdrawing
.. _QuickDrawData: https://quickdraw.readthedocs.io/en/latest/api.html#quickdrawdata
.. _QuickDrawDataGroup: https://quickdraw.readthedocs.io/en/latest/api.html#quickdrawdatagroup
.. _drawing_names: https://quickdraw.readthedocs.io/en/latest/api.html#quickdraw.QuickDrawDataGroup.drawing_names
.. _drawings: https://quickdraw.readthedocs.io/en/latest/api.html#quickdraw.QuickDrawDataGroup.drawings
.. _issues: https://github.com/martinohanlon/quickdraw_python/issues
.. _github repository: https://github.com/martinohanlon/quickdraw_python
