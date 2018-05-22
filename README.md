# PyDualDDS

Dual channel sinewave DDS from 0-4 GHz based on the DAC38RF82EVM.

This Python library allows to interface with the DAC38RF82EVM evaluation
board. It is designed to control the numercially controlled oscillators (NCOs)
to generate two independent sinewave signals in stand-alone-mode, no FPGA card
required. However, it is not limited to this use only, every other register on
the board can be written and read with this library. The two channels can each
be controlled in frequency (0-4 GHz), phase (0-360 degrees), and amplitude (2048
steps).

# Full Documentation

Read the file PyDualDDS.pdf. The documentation is also available in docs/_build/
both as html and pdf format.

# How to Cite

If you use this software in your research, please consider citing it like:

Andreas Fognini PyDualDDS. Available at https://github.com/afognini/.

# Authors, Copyright, License

Authors: Andreas Fognini

Copyright (C) Andreas Fognini

Released under the terms of the GPLv3 License (see file LICENSE)

# Acknowledgement

A. Fognini greatly acknowledges the support from the Swiss National Science
Foundation's Early Postdoc Fellowship.

# Requirements

Please note that this library needs Python 3.5 or larger, and pyftdi.
