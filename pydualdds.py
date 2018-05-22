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

import time
from pyftdi import gpio

class DDS(object):
    """The DDS library controls the DAC38RF82EVM board and implements a two channel DDS from 0-4 GHz.

        The frequency, the phase, and amplitude of each channel can be independently controlled.

        The DAC is configured to run at 8.847 Giga samples per second from the on borad's 122.88 MHz clock.

        This library allows to use the board in standalone mode without an additional FPGA card.
    """
    def __init__(self, config="./config/PLL_M9N5Ref1228_8MHz_PLLlock.cfg"):
        """Initialize the library

            :param str config: Path to configuration file
        """
        self.dac=DacCom(config=config)
        self.DAC_SAMPLING_RATE = 1228.8*9*4/5

    def config_board(self):
        """Configures the DAC and the clock distribution chip on the board

        Resets the DAC by its reset pin and loads the configuration file in to the DAC and the clock distribution chip.
        """
        self.dac.dac_reset()
        print("Configuring clock generation...")
        self.dac.lmk_configure()
        print("done")
        print("Configuring DAC38RF82...")
        self.dac.dac_configure()
        print("done")

    def start_up_sequence(self):
        """Start up sequence

        Starts up the PLLs, resets the chips, and synchronizes via SYSREF.
        """
        self.dac.lmk_write(0x0139,0x00)
        self.dac.lmk_write(0x0143,0x11)
        self.dac.lmk_write(0x0144,0x7E)
        self.dac.lmk_write(0x0144,0x7C)
        self.dac.lmk_write(0x0143,0x31)
        self.dac.lmk_write(0x0143,0x11)
        self.dac.lmk_write(0x0144,0xFC)
        self.dac.lmk_write(0x0144,0xFD)
        self.dac.lmk_write(0x0144,0xFF)
        self.dac.lmk_write(0x0139,0x03)
        self.dac.lmk_write(0x010E,0x70)
        self.dac.lmk_write(0x0106,0x70)

        self.dac.dac_write(0x0124,0x00)
        self.dac.dac_write(0x0224,0x00)
        self.dac.dac_write(0x015C,0x00)
        self.dac.dac_write(0x025C,0x00)
        self.dac.dac_write(0x040A,0xFC03)
        self.dac.dac_write(0x040A,0x7C03)
        self.dac.dac_write(0x0000,0x5801)
        self.dac.dac_write(0x0000,0x5803)

        self.dac.dac_write(0x0124,0x30)
        self.dac.dac_write(0x0224,0x20)
        self.dac.dac_write(0x015C,0x2)
        self.dac.dac_write(0x025C,0x3)
        self.dac.dac_write(0x0000,0x5801)
        self.dac.dac_write(0x0000,0x5800)

        self.dac.lmk_write(0x010E,0x71)
        self.dac.lmk_write(0x0106,0x71)

        self.dac.dac_write(0x0128,0x0332)
        self.dac.dac_write(0x0128,0x0330)
        self.dac.dac_write(0x0228,0x0332)
        self.dac.dac_write(0x0228,0x0330)

    def nco_freq_a(self, freq):
        """Set frequency of channel A's NCO.

        :param float freq: Frequency in MHz
        """
        freq_bin=int(0xFFFFFFFFFFFF*freq/float(self.DAC_SAMPLING_RATE))
        self.dac.dac_write(0x011E,freq_bin%0x10000)
        self.dac.dac_write(0x011F,freq_bin%0x100000000>>16)
        self.dac.dac_write(0x0120,freq_bin%0x1000000000000>>32)

        #Path CD
        self.dac.dac_write(0x0121,0x0)
        self.dac.dac_write(0x0122,0x0)
        self.dac.dac_write(0x0123,0x0)

        self._trigger_spi()

    def nco_freq_b(self, freq):
        """Set frequency of channel B's NCO.

        :param float freq: Frequency in MHz
        """
        freq_bin=int(0xFFFFFFFFFFFF*freq/float(self.DAC_SAMPLING_RATE))
        self.dac.dac_write(0x021E,freq_bin%0x10000)
        self.dac.dac_write(0x021F,freq_bin%0x100000000>>16)
        self.dac.dac_write(0x0220,freq_bin%0x1000000000000>>32)

        #Path CD
        self.dac.dac_write(0x0221,0x0)
        self.dac.dac_write(0x0222,0x0)
        self.dac.dac_write(0x0223,0x0)

        self._trigger_spi()

    def _trigger_spi(self):
        """Trigger SPI
        """
        self.dac.dac_write(0x0328,0x330)
        self.dac.dac_write(0x0328,0x332)
        self.dac.dac_write(0x0328,0x330)

    def nco_sync(self):
        """Synchronize NCO's by asserting SYSREF

           Call this function after a frequecy change to resynchronize the phase.
        """
        self.dac.lmk_write(0x0139,0x00)
        self.dac.lmk_write(0x0143,0x11)
        self.dac.lmk_write(0x0144,0x7E)
        self.dac.lmk_write(0x0144,0x7C)
        self.dac.lmk_write(0x0143,0x31)
        self.dac.lmk_write(0x0143,0x11)
        self.dac.lmk_write(0x0144,0xFC)
        self.dac.lmk_write(0x0144,0xFD)
        self.dac.lmk_write(0x0144,0xFF)
        self.dac.lmk_write(0x0139,0x03)
        self.dac.lmk_write(0x010E,0x70)
        self.dac.lmk_write(0x0106,0x70)
        self.dac.lmk_write(0x010E,0x71)
        self.dac.lmk_write(0x0106,0x71)

    def nco_phase_a(self, deg):
        """Set phase of channel A's NCO.

        :param float deg: Phase in degrees
        """
        phase_bin=int(deg/360.0*0xFFFF)
        self.dac.dac_write(0x011C,phase_bin)

        #Phase CD
        self.dac.dac_write(0x011D,0)
        self._trigger_spi()

    def nco_phase_b(self, deg):
        """Set phase of channel B's NCO.

        :param float deg: Phase in degrees
        """
        phase_bin = int(deg/360.0*0xFFFF)
        self.dac.dac_write(0x021C,phase_bin)

        #Phase CD
        self.dac.dac_write(0x021D,0)
        self._trigger_spi()

    def amplitude_a(self, gain):
        """Amplitude of channel A.

        :param float gain: Amplitude setting (0-2)

        Above gain 1 distortions may accure. Allows 1024 steps in the gain range from 0-1.
        """
        gain_hex = int(gain/2.0*(2**11-1))
        self.dac.dac_write(0x0132, gain_hex | 0x8000) #Enable gain and choose gain

    def amplitude_b(self, gain):
        """Amplitude of channel B.

        :param float gain: Amplitude setting (0-2)

        Above gain 1 distortions may accure. Allows 1024 steps in the gain range from 0-1.
        """
        gain_hex = int(gain/2.0*(2**11-1))
        self.dac.dac_write(0x0232, gain_hex | 0x8000) #Enable gain and choose gain

class DacCom(object):
    def __init__(self, config = "./config/PLL_M9N5Ref1228_8MHz_PLLlock.cfg"):
        self.LMK_CONFIG = self.read_lmk_config(config)
        self.DAC_CONFIG = self.read_dac_config(config)

        self.LMK_SCK  = int('10000',2)
        self.LMK_SDIO = int('100000',2)
        self.LMK_SDO  = int('1000000',2)
        self.LMK_CS   = int('10000000',2)

        self.DAC_SCK   = int('1',2)
        self.DAC_SDIO  = int('10',2)
        self.DAC_SDO   = int('100',2)
        self.DAC_SDENB = int('1000',2)

        self.DAC_PAGE_ADR = 0x09
        self.DAC_PAGE = 0 #keep track of register pages to speed up communication

        self.PORT = 0
        self.DEBUG = True

        self.gpio_dac = gpio.GpioController()
        self.gpio_dac.open_from_url('ftdi://ftdi:2232h/1',direction=int('11111111',2))

        self.gpio = gpio.GpioController()
        self.gpio.open_from_url('ftdi://ftdi:2232h/2',direction=int('11111111',2))


        #Set CS of LMK to 1
        self.gpio.write_port(self.LMK_CS)
        self.PORT=self.LMK_CS
        self.set_bit_on_port(self.DAC_SDENB, True)
        self.set_bit_on_port(self.DAC_SCK, False)
        self.port_flush()

    def dac_reset(self):
        """Reset the DAC
        """
        self.gpio_dac.write_port(int('00000000',2))
        self.gpio_dac.write_port(int('00100000',2))

    def lmk_configure(self):
        """Configure the LMK04828 clock cleaner from the provided configuration file

            :raises ValueError: if the read value does not correspond to the set value
        """

        if self.DEBUG:
            print("Adr:\tSet:\tRead:")
        for d in self.LMK_CONFIG:
            self.lmk_write(d['adr'],d['value'])
            read_back =self.lmk_read(d['adr'])
            if self.DEBUG:
                print(str(d['adr'])+ "\t" + str(d['value']) +'\t'+str(read_back) )
            if read_back!=d['value']:
                raise ValueError('LMK configuration, set value not equal to read back value')

    def dac_configure(self):
        """Configure the DAC from the provided configuration file.

            :raises ValueError: if the read value does not correspond to the set value
        """
        if self.DEBUG:
            print("Adr:\tSet:\tRead:")
        for i in range(len(self.DAC_CONFIG)):
            d = self.DAC_CONFIG[i]
            self.dac_write(d['adr'],d['value'])
            read_back =self.dac_read(d['adr'])
            if self.DEBUG:
                print(str(hex(d['adr']))+ "\t" + str(hex(d['value'])) +'\t'+str(hex(read_back)) )
            if read_back!=d['value'] and d['adr']!=0:
                raise ValueError('DAC configuration, set value not equal to read back value')

    def read_lmk_config(self, file_name):
        """Read the configuration file and extract the LMK04828 data from it.

            :param str file_name: Path to the configuration file
            :return: LMK04828 configuration dictionary
        """
        f_config = open(file_name,'r')
        LMK_CONFIG = []
        with open(file_name,'r') as f:
            for line in f:
                if 'DAC_RESET' in line:
                    break
                d = line.strip().split()
                if len(d)>1:
                    #print(str(d[0])+ "\t" + str(d[1]))
                    #print(str(int(d[0],16))+ "\t" + str(int(d[1],16)))
                    LMK_CONFIG.append({'adr':int(d[0],16), 'value':int(d[1],16)})

        return LMK_CONFIG

    def read_dac_config(self, file_name):
        """Read the configuration file and extract the DAC data from it.

            :param str file_name: Path to the configuration file
            :return: DAC configuration dictionary
        """
        DAC_CONFIG = []
        #Seek DAC38RF8x in file
        found_dac_description =False
        with open(file_name,'r') as f:
            for line in f:
                if found_dac_description:
                    d=line.strip().split()
                    if len(d)>1:
                        DAC_CONFIG.append({'adr':int(d[0],16), 'value':int(d[1],16)})

                if "DAC38RF8x" in line.strip().split():
                    found_dac_description =True

        return DAC_CONFIG

    def set_bit(self, bits, position, value):
        """Set bit in bit field bits at a given position to a specified value.

            Helper function.

            :param int bits: bit field
            :param int position: bit field e.g. 0b11110000
            :param int value: number e.g. 5
            :return: Changed bit field
        """
        bit_selector = position
        bits &= ~bit_selector
        bits |= bit_selector*value
        return bits

    def set_bit_on_port(self, bit, value):
        """Set a bit of the 8 bit output port

            :param int bit: bit position 0-7
            :param bool value: True or False
        """
        self.PORT = self.set_bit(self.PORT, bit, value)

    def port_flush(self):
        """Flush data to port.
        """
        self.gpio.write_port(self.PORT)

    def dac_write(self, address, data):
        """Write a DAC register

            :param int address: Address of register to write in
            :param int data: data to write to register
        """
        #Get page from address
        page = address>>8
        address_without_page = address%0x100

        self.dac_change_page(page)
        self.dac_write_byte(address_without_page, data)

    def dac_change_page(self, page):
        """Change register mapping page.

            The registers are devided in three pages: multi-DUC1 (0b001), multi-DUC2 (0b010), and DIG_MISC (0b100).

            Multiple pages can be written at the same time, i.e. 0x011 writes multi-DUC1 and multi-DUC2 at the same time.

            Function keeps track of the selected pages in variable self.DAC_PAGE.

            :param int page: 0b000 - 0b111
        """

        #write page only if not set already, for speed up
        if self.DAC_PAGE != page:
            self.DAC_PAGE = page
            self.dac_write_byte(self.DAC_PAGE_ADR, page)

    def dac_write_byte(self, address, data):
        """Write a byte to the DAC.

            :param int address: Address of register with page prefix, e.g 0x0328 writes the register 0x28 of page multi-DUC1 and multi=DUC2 at the same time.
            :param int data: data to write to register (0x00-0xFF)
        """
        self.gpio.set_direction(0xFF, 0xFF)

        self.set_bit_on_port(self.DAC_SCK, False)
        self.port_flush()

        RW = 0

        send = RW*2**23 + address*2**16 + data

        mask = 1*2**23

        #Clock low CS low
        self.set_bit_on_port(self.DAC_SDENB, False)
        self.port_flush()

        while mask > 0:
            send_bit = (mask & send) > 0
            #Write data bit
            self.set_bit_on_port(self.DAC_SCK, False)
            self.port_flush()

            self.set_bit_on_port(self.DAC_SDIO, send_bit)
            self.port_flush()

            #Clock it out
            self.set_bit_on_port(self.DAC_SCK, True)
            self.port_flush()
            mask = mask >> 1

        #Clock High CS low
        self.set_bit_on_port(self.DAC_SCK, False)
        self.set_bit_on_port(self.DAC_SDENB, True)
        self.port_flush()

    def dac_read(self, address):
        """Read a register from the DAC.

            :param int address: Address of register with page prefix, e.g 0x0128 reads the register 0x28 of page multi-DUC1.
            :return: Register value
        """
        #Get page from address
        page = address >> 8
        address_without_page = address % 0x100

        self.dac_change_page(page)
        return self.dac_read_byte(address_without_page)

    def dac_read_byte(self, address):
        """Read a register from the DAC without page correction.

            :param int address: Address of register
            :return: Register value
        """
        self.set_bit_on_port(self.DAC_SCK, False)
        self.port_flush()

        RW = 1
        send = RW*2**(7) + address

        self.set_bit_on_port(self.DAC_SDENB, False)
        self.port_flush()

        mask = 1*2**7

        while mask > 0:
            self.set_bit_on_port(self.DAC_SCK, False)
            self.port_flush()

            send_bit = (mask & send) > 0
            #Write data bit
            self.set_bit_on_port(self.DAC_SDIO, send_bit)
            self.port_flush()

            #Clock it out

            self.set_bit_on_port(self.DAC_SCK, True)
            self.port_flush()
            mask = mask >> 1

        self.gpio.set_direction(0xFF, 0b11111001)
        self.set_bit_on_port(self.DAC_SDIO, False) #Can't set a value which is on read mode
        self.set_bit_on_port(self.DAC_SDO, False) #Can't set a value which is on read mode

        data = 0
        mask = 1*2**15
        while mask > 0:
            self.set_bit_on_port(self.DAC_SCK, False)
            self.port_flush()
            self.set_bit_on_port(self.DAC_SCK, True)
            self.port_flush()
            port = self.gpio.read_port()
            bit = (port & self.DAC_SDO) > 0

            data = data | mask*bit

            mask = mask >> 1

        #Clock High CS low
        self.set_bit_on_port(self.DAC_SCK, False)
        self.port_flush()
        self.set_bit_on_port(self.DAC_SDENB, True)
        self.port_flush()

        self.gpio.set_direction(0xFF, 0xFF)
        return data

    def lmk_write(self, address, data):
        """Write data to a address in the LMK04828.

            :param int address: Address of register
            :param int data: data
        """
        self.gpio.set_direction(0xFF, 0xFF)
        RW = 0
        W1 = 0
        W0 = 0

        send = RW*2**23+W1*2**22+W0*2**21+address*2**8+data

        mask = 1*2**23

        #Clock low CS low
        self.set_bit_on_port(self.LMK_SCK, False)
        self.set_bit_on_port(self.LMK_CS, False)
        self.port_flush()

        while mask > 0:
            send_bit = (mask & send) > 0
            #Write data bit
            self.set_bit_on_port(self.LMK_SCK, False)
            self.port_flush()

            self.set_bit_on_port(self.LMK_SDIO, send_bit)
            self.port_flush()

            #Clock it out
            self.set_bit_on_port(self.LMK_SCK, True)
            self.port_flush()
            mask = mask >> 1

        #Clock High CS low
        self.set_bit_on_port(self.LMK_SCK, True)
        self.set_bit_on_port(self.LMK_CS, True)
        self.port_flush()

    def lmk_read(self, address):
        """Read data from an address of the LMK04828

            :param int address: Address of register
            :return: Data at address
        """

        RW = 1
        W1 = 0
        W0 = 0

        send = RW*2**(23-8) + W1*2**(22-8) + W0*2**(21-8) + address

        mask = 1*2**(23-8)

        #Clock low CS low
        self.set_bit_on_port(self.LMK_SCK, False)
        self.set_bit_on_port(self.LMK_CS, False)
        self.port_flush()

        while mask > 0:
            self.set_bit_on_port(self.LMK_SCK, False)
            self.port_flush()

            send_bit = (mask & send) > 0
            #Write data bit
            self.set_bit_on_port(self.LMK_SDIO, send_bit)
            self.port_flush()

            #Clock it out
            self.set_bit_on_port(self.LMK_SCK, True)
            self.port_flush()
            mask = mask >> 1

        self.gpio.set_direction(0xFF, 0b11011111)
        self.set_bit_on_port(self.LMK_SDIO, False) #Can't set a value which is on read mode
        self.set_bit_on_port(self.LMK_SCK, False)
        self.port_flush()
        self.set_bit_on_port(self.LMK_SCK, True)
        self.port_flush()

        data = 0
        mask = 1*2**7
        while mask > 0:
            port = self.gpio.read_port()
            bit = (port & self.LMK_SDIO) > 0
            #print(bit)

            data = data | mask*bit
            self.set_bit_on_port(self.LMK_SCK, False)
            self.port_flush()
            self.set_bit_on_port(self.LMK_SCK, True)
            self.port_flush()
            mask = mask >> 1

        #Clock High CS low
        self.set_bit_on_port(self.LMK_SCK, True)
        self.port_flush()
        self.set_bit_on_port(self.LMK_CS, True)
        self.port_flush()

        self.gpio.set_direction(0xFF, 0xFF)
        return data

    def close(self):
        """Close the connection to the DAC card.
        """
        self.gpio.close()

if __name__ =="__main__":
    #Example Program
    #Configures the board and outputs on both channel frequency of 397.76 MHz with the same amplitude.
    d=DDS()
    d.config_board()

    d.start_up_sequence()

    d.nco_freq_a(397.76)
    d.nco_freq_b(397.76)
    d.nco_phase_a(0)
    d.nco_phase_b(0)

    #SYSREF Trigger to synchornize channel A and B, should be
    #Should be executed after each frequency change to the NCOs if the phase matters between them.
    d.nco_sync()

    #Setting amplitude
    d.amplitude_a(1)
    d.amplitude_b(1)
