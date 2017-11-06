#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2017 Andreas Fognini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pydualdds import DDS

dac = DDS()
dac.config_board()

dac.start_up_sequence()

dac.nco_freq_a(397.76)
dac.nco_freq_b(397.76)
dac.nco_phase_a(0)
dac.nco_phase_b(0)

#SYSREF Trigger to synchronize channel A and B, should be
#Should be executed after each frequency change to the NCOs if the phase matters between them.
dac.nco_sync()

#Setting amplitude
dac.amplitude_a(1)
dac.amplitude_b(1)
