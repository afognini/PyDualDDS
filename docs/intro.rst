***************
Introduction
***************

Dual channel sine wave Direct Digital Synthesizer (DDS) from 0-4 GHz based on the DAC38RF82EVM.

This Python library allows to interface with the DAC38RF82EVM evaluation board. It is designed to control the numerically controlled oscillators (NCOs) to generate two independent sine wave signals in standalone mode, no FPGA card required. However, it is not limited to this use only, every register on the board can be written and read with this library too. The two output channels can each be independently controlled in frequency (0-4 GHz), phase (0-360 degrees), and amplitude (2048 steps).

Motivation
=================

For a quantum optics experiment we needed a two channel phase and frequency controllable sine wave generator to drive an electro-optical-modulator at around 400 MHz.
The software from TI does not readily allow to control the card through an API. Therefore, we have developed a control library of our own.

Setting up the card for standalone mode
===============================================

To use the card in standalone mode, the card has to be configured to use the on board 122.88 MHz oscillator.
For that the jumpers have to be set as follows:

======  =============   ===========
Jumper  Position        Description
======  =============   ===========
JP1     Shunt pin 2-3   Disable DAC sleep mode
JP2     Shunt pin 1-2   Enable DAC output
JP3     Close           Enable on board 122.88 MHz oscillator
JP8     Open            Enable VDDDIG1 supply
JP9     Open            Enable VEE18N supply
JP10    Open            Enable PLL clock mode
======  =============   ===========

The library will configure the clock distribution chip (LMK04828) to generate a 1228.8 MHz = 10*122.88 MHz reference clock for the DAC38RF82. Subsequently, the DAC38RF82's internal PLL will be configured to generate the DAC's sampling rate running at 8847.36 MHz = 1228.8 MHz*9*4/5.

Usage of the library
==============================
The usage of the library is outlined in an example of setting both output channels
to 397.76 MHz, zero phase, and an amplitude of 1.

.. code-block:: python

	from pydualdds import DDS

	dac = DDS()
	dac.config_board()

	dac.start_up_sequence()

The board is configured from the configuration file and properly initialized in the startup sequence.

.. code-block:: python

	#Setting the frequency
	dac.nco_freq_a(397.76)
	dac.nco_freq_b(397.76)

	#Setting the phase
	dac.nco_phase_a(0)
	dac.nco_phase_b(0)

	#Setting the amplitude
	dac.amplitude_a(1)
	dac.amplitude_b(1)

Then both channels (A and B) are set to 397.76 MHz with a relative phase of zero and amplitude 1.
To set the phase the SYSREF needs to be triggered to synchronize the two NCOs:

.. code-block:: python

	dac.nco_sync()

This code example in full is found in the file 'example.py'.
