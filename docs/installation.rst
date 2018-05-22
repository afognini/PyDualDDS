***************
Installation
***************

Before you can start the installation of the PyDualDDS library you have to
install the pyftdi library.

Please note that on Linux you have to set permissions to be able to access the
USB interface, see http://eblot.github.io/pyftdi/installation.html.  In short,
create the following rules file for udev::

  /etc/udev/rules.d/10-ftdi.rules
  ---
  SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", GROUP="plugdev", MODE="0666"

Then, ensure the new rules are reloaded and triggered::

  $ sudo udevadm control --reload-rules
  $ sudo udevadm trigger

and finally add the user to the plugdev group::

  $ sudo gpasswd -a USER plugdev

Log out then log in again for the new group attributes to take effect.  If the
DAC is already plugged in, remove it and then plug it in again.  This time
`udev` will add the USB device with user-accessible permissions.

Once the pyftdi library is installed you can proceed installing the PyDualDDS
library. Open a terminal and navigate in to the PyDualDDS folder.

Then install it either by::

	sudo python setup.py install

or by::

	sudo python3 setup.py install

depending on your python installation. Note, PyDualDDS needs Python 3.5 or higher.

You can test if the installation worked by importing the library:

.. code-block:: python

	import pydualdds

If you not getting an error message, everything worked out.
