"""
###########################################################
# Filename: AD5235.py
# Description:
#   Control digital resistor AD5235
#   capable to control daisy chain
#
# Author: [Aleksandr Chasnyk]
# Created: [2024.01.23]
# Last modified: [Date last modified]
# Python Version: [>3]
#
# Description:
## Define default
spi_freq = 1000000  # SPI frequency in Hz
cs_pin = 9  # GPIO pin for Chip Select (CS)
sck_pin = 10  # GPIO pin for SPI Clock (SCK)
mosi_pin = 11  # GPIO pin for SPI Master Out Slave In (MOSI)
miso_pin = 8  # GPIO pin for SPI Master In Slave Out (MISO)

#
###########################################################
"""

import machine
import time
from micropython import const
from rp2 import PIO, asm_pio
#default values
miso_def = 8  # GPIO pin for SPI Master In Slave Out (MISO)
cs_def = 9  # GPIO pin for Chip Select (CS)
sck_def = 10  # GPIO pin for SPI Clock (SCK)
mosi_def = 11  # GPIO pin for SPI Master Out Slave In (MOSI)
spi_def = 1
n_devs = 4
def range_check(val, min_val, max_val):
    # Ensure val is within the specified range
    val = max_val if val > max_val else val  # If val is greater than max_val, set it to max_val, otherwise keep it unchanged
    val = min_val if val < min_val else val  # If val is less than min_val, set it to min_val, otherwise keep it unchanged
    return val  # Return the adjusted value


class AD5235_class:

    def __init__(self, spi=spi_def, sck_pin=sck_def, mosi_pin=mosi_def, miso_pin=miso_def, cs_pin=cs_def, daisy_chain=n_devs):
        '''
        Initialization of class
        :param spi: for RP2040 available 0 or 1
        :param sck_pin: clock pin
        :param mosi_pin: MOSI pin
        :param miso_pin: MISO pin
        :param cs_pin: chip select
        :param daisy_chain: min 1 max 4
        '''
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)
        self.cs.high()
        # # Initialize SPI
        # bits = 8
        # bits =  16 experimental to check
        self.spi = machine.SPI(spi,
                               baudrate=1_000_000,
                               sck=machine.Pin(sck_pin),
                               mosi=machine.Pin(mosi_pin),
                               miso=machine.Pin(miso_pin),
                               polarity=0,
                               phase=0,
                               bits=8)

        self._dev_adr = [0, 1] * daisy_chain  # there is 2 resistors in one IC packages
        buffer = [0] * daisy_chain * 2
        self._buf_set_res = buffer.copy()  # buffer for setting resistor value in ADC counts
        self._buf_rd = buffer.copy()  # buffer for reading current start of wiper position in ADC count
        self.buf1_cmd_spi = [0]*daisy_chain*3 # 3 bytes per 1 device
        self.buf2_cmd_spi = [0]*daisy_chain*3 # 3 bytes per 1 device


    def write_to_dev(self):
        '''
        Write value buffer to device
        :return: None
        '''
        # print(self._buf_rd)
        # Select the ADC
        self._fill_cmd_buf()
        # Send command to read ADC data
        # print("Write to dev")
        # # print(self.buf_cmd)
        # # print(self._buf_cmd_spi) # for debug only
        print("RES: ",self._buf_set_res)
        print("1: ",self.buf1_cmd_spi)  # for debug only
        print("2: ", self.buf2_cmd_spi)  # for debug only
        # # buf1, buf2 = self._split_odd_even()

        command1 = bytes(self.buf1_cmd_spi)  # Replace with the actual command bytes
        command2 = bytes(self.buf2_cmd_spi)  # Replace with the actual command bytes
        self.cs.low() # Select the Chip select
        self.spi.write(command1) # write buffer
        self.cs.high() # Deselect the Chip select
        self.cs.low()  # Select the Chip select
        self.spi.write(command2)  # write buffer
        self.cs.high()  # Deselect the Chip select


    # def query(self, cmd_array):
    # def set_rdaq(self, ch, val):
    def set_raw_val(self, position, reg_cnt):
        '''
        Setting direct register value from 0 to 1023
        :param position: position of resistor. IC0->0,1; IC1->2,3; IC3->4,5; IC4->6,7
        :param reg_cnt: register value from 0 to 1023
        :return: none
        '''
        position = range_check(position, 0, len(self._dev_adr) - 1)  # Ensure position is within the valid range
        reg_cnt = int(range_check(reg_cnt, 0, 1023))  # Ensure reg_cnt is within the range of 0 to 1023
        self._buf_set_res[position] = reg_cnt  # Set the specified position in the buffer to reg_cnt
        return self._buf_set_res  # Return the updated buffer for setting resistor values

    def set_Ohm_val(self, position, res_in_Ohm):
        '''
        Setting resistor value  register value from 0 to 1023
        :param position: position of resistor. IC0 -> 0,1; IC1 ->2,3; IC3 -> 4,5; IC4 -> 6,7
        :param reg_val: register value from 0 to 1023
        :return: none
        '''
        return self.set_raw_val(position, self._get_adc_val_from_res_val(res_in_Ohm))

    #####################################
    # Only for testing
    #####################################
    def test_buffer(self):
        self._fill_cmd_buf()
        hex_array_1 = [hex(value) for value in self._buf_set_res]
        # hex_array_2 = [hex(value) for value in self.buf_cmd]
        # hex_array_3 = [value for value in self._buf_cmd_spi]
        print(hex_array_1)
        # print(hex_array_2)
        # print(hex_array_3)

    @property
    def get_res_buffer(self):
        return self._buf_set_res
    #####################################
    # private methods
    #####################################
    def _fill_cmd_buf(self):
        '''
        fill in command buffer from value buffer for each resistor in chain
        :return: buf_cmd_spi
        '''
        cmd = []
        cmd1 = []
        cmd2 = []
        # creating command list for AD5235
        # slitting command list into two list
        # only because AD5235 support single SPI command
        # Value for 1 resistor in Chain should be written in first go
        # value for second resistor in chain should be written in another go
        for index, value in enumerate(self._buf_set_res):
                cmd.append(self._get_command("wrt", self._dev_adr[index], value))
        cmd1 = cmd[0::2]
        cmd2 = cmd[1::2]
        cmd = []
        for item in cmd1:
            cmd.append(self._convert_to_8bits(item))  # by default 8 bit operation
        #  cmd.append(self._convert_to_16bits(item)) # need to check if 16 operation possible
        # make flat array from array of arrays
        # print(cmd)
        self.buf1_cmd_spi = [item for array in cmd for item in array]

        cmd = []
        for item in cmd2:
            cmd.append(self._convert_to_8bits(item))  # by default 8 bit operation
        #  cmd.append(self._convert_to_16bits(item)) # need to check if 16 operation possible
        # make flat array from array of arrays
        self.buf2_cmd_spi = [item for array in cmd for item in array]


    def _get_command(self, cmd="nop", ch=0, data=0):
        cmd_nop = const(0x00)
        cmd_wrt_rdac = const(0b10110000)  # cmd 11 datasheet
        cmd_store_wiper_eemem = const(0b00100000)
        cmd_rd_rdac = const(0b10100000)
        data = int(range_check(data, 0, 1024))
        ch = int(range_check(ch, 0, 1))
        # set cmd then
        cmd_var = {
            "wrt": cmd_wrt_rdac,
            "rd": cmd_rd_rdac,
            "srt_wiper": cmd_store_wiper_eemem
        }.get(cmd, cmd_nop)

        adc_value = (cmd_var << 16) | (ch << 16) | data
        return adc_value

    def _convert_to_8bits(self, value):
        '''
        converting array of 24bits back into 8 bit for SPI send register
        :return: array of 3 values by 8 bits each
        '''
        byte1 = (value >> 16) & 0xFF
        byte2 = (value >> 8) & 0xFF
        byte3 = value & 0xFF
        return [byte1, byte2, byte3]

    def _convert_to_16bits(self, value):
        '''
        converting array of 24bits back into 16 bit for SPI send register
        :return: array of 2 values by 16 bits each
        '''
        byte1 = (value >> 16) & 0xFFFF
        byte2 = value & 0xFFFF
        return [byte1, byte2]

    def _get_adc_val_from_res_val(self, res_Ohm):
        res_Ohm = range_check(res_Ohm, 0, 249900)
        Rw = 50  # wiper resistance, datasheet
        Rab = 250000  # full scale resistance 250k -> in Ohm
        cnt = 1024 * (res_Ohm - Rw) / Rab
        cnt = int(round(cnt, 0))
        return cnt



