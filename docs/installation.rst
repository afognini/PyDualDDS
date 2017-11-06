***************
Installation
***************

Before you can start the installation of the PyDualDDS library you have to install the pyftdi library.

Please note that on Linux you have to set permissions to be able to access the USB interface, see http://eblot.github.io/pyftdi/installation.html.

Once the pyftdi library is installed you can proceed installing the PyDualDDS library. Open a terminal and navigate in to the PyDualDDS folder.

Then install it either by::

	sudo python setup.py install

or by::

	sudo python3 setup.py install

depending on your python installation. Note, PyDualDDS needs Python 3.5 or higher.

You can test if the installation worked by importing the library:

.. code-block:: python

	import pydualdds

If you not getting an error message, everything worked out.
