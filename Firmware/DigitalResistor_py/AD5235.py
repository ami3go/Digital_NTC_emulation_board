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
import micropython
import machine
import time
from micropython import const
from rp2 import PIO, asm_pio

# default values

miso_def = 8  # GPIO pin for SPI Master In Slave Out (MISO)
cs_def = 9  # GPIO pin for Chip Select (CS)
sck_def = 10  # GPIO pin for SPI Clock (SCK)
mosi_def = 11  # GPIO pin for SPI Master Out Slave In (MOSI)
spi_def = 1 # SPI interface number, 0 or 1
n_devs = 4  # number of AD5235 device connected in daisy chain
rdy_def = 12
rdy = machine.Pin(rdy_def, machine.Pin.IN, machine.Pin.PULL_UP)
r_ab_val = 250000  # Full scale resistance 10000 or 250000


def range_check(val, min_val, max_val):
    # Ensure val is within the specified range
    val = max_val if val > max_val else val  # If val is greater than max_val, set it to max_val, otherwise keep it unchanged
    val = min_val if val < min_val else val  # If val is less than min_val, set it to min_val, otherwise keep it unchanged
    return val  # Return the adjusted value


class AD5235_class:

    def __init__(self, spi=spi_def, sck_pin=sck_def, mosi_pin=mosi_def, miso_pin=miso_def, cs_pin=cs_def, daisy_chain=n_devs, r_ab=r_ab_val):
        '''
        Initialization of class
        :param spi: for RP2040 available 0 or 1
        :param sck_pin: clock pin
        :param mosi_pin: MOSI pin
        :param miso_pin: MISO pin
        :param cs_pin: chip select
        :param daisy_chain: min 1 max 4
        '''
        self.Rab = const(r_ab)
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

    @micropython.native
    def write_resistance(self):
        '''
        Write value buffer to device
        :return: None
        '''
        self._fill_cmd_buf("wrt", self._buf_set_res)
        print("RES: ",self._buf_set_res)
        print("1: ", self.buf1_cmd_spi)  # for debug only
        print("2: ", self.buf2_cmd_spi)  # for debug only
        self._spi_write(self.buf1_cmd_spi)
        self._spi_write(self.buf2_cmd_spi)



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
        :param res_in_Ohm: resistance in Ohm from 0 to 250k
        :return: none
        '''
        return self.set_raw_val(position, self._get_adc_val_from_res_val(res_in_Ohm))


    @property
    def get_res_buffer(self):
        return self._buf_set_res

    def store_wiper_to_eemem(self):
        data = [1]*8
        self._fill_cmd_buf("srt_wiper", data)
        print("1: ", self.buf1_cmd_spi)  # for debug only
        print("2: ", self.buf2_cmd_spi)  # for debug only
        self._spi_write(self.buf1_cmd_spi)
        self._spi_write(self.buf2_cmd_spi)

    def restore_wiper(self):
        data = [0] * 8
        self._fill_cmd_buf("resrt_wiper", data)
        print("1: ", self.buf1_cmd_spi)  # for debug only
        print("2: ", self.buf2_cmd_spi)  # for debug only
        self._spi_write(self.buf1_cmd_spi)
        self._spi_write(self.buf2_cmd_spi)

    #####################################
    # private methods
    #####################################
    def _fill_cmd_buf(self, spi_cmd, buffer):
        '''
        fill in command buffer from value buffer for each resistor in chain
        :return: buf_cmd_spi
        '''
        cmd = []
        # creating command list for AD5235
        # splitting command list into two list
        # only because AD5235 support single SPI command
        # Value for 1 resistor in Chain should be written in first go
        # value for second resistor in chain should be written in another go
        for index, value in enumerate(buffer):
            cmd.append(self._get_command(spi_cmd, self._dev_adr[index], value))
        self.buf1_cmd_spi = self._convert_to_8bit_arrya(cmd[0::2])
        self.buf2_cmd_spi = self._convert_to_8bit_arrya(cmd[1::2])


    @micropython.native
    def _get_command(self, cmd="nop", ch=0, data=0):
        cmd_nop = const(0x00)
        cmd_wrt_rdac = const(0b10110000)  # cmd 11 datasheet
        cmd_store_wiper_eemem = const(0b00100000)
        cmd_restore_wiper_eemem = const(0b00010000)
        cmd_rd_rdac = const(0b10100000)
        cmd_reset = const(0b10000000)
        data = int(range_check(data, 0, 1024))
        ch = int(range_check(ch, 0, 1))
        # set cmd then
        cmd_var = {
            "wrt": cmd_wrt_rdac,
            "rd": cmd_rd_rdac,
            "srt_wiper": cmd_store_wiper_eemem,
            "resrt_wiper": cmd_restore_wiper_eemem,
            "rst": cmd_reset
        }.get(cmd, cmd_nop)

        adc_value = (cmd_var << 16) | (ch << 16) | data
        return adc_value

    @micropython.native
    def _convert_to_8bits(self, value):
        '''
        converting array of 24bits back into 8 bit for SPI send register
        :return: array of 3 values by 8 bits each
        '''
        byte1 = (value >> 16) & 0xFF
        byte2 = (value >> 8) & 0xFF
        byte3 = value & 0xFF
        return [byte1, byte2, byte3]
    def _convert_to_8bit_arrya(self, in_array):
        '''
        converting array of 24bits back into 8 bit for SPI send register
        :return: array of 3 values by 8 bits each
        '''
        ret_val = []
        for value in in_array:
            ret_val.append((value >> 16) & 0xFF)
            ret_val.append((value >> 8) & 0xFF)
            ret_val.append(value & 0xFF)
        return ret_val

    @micropython.native
    def _convert_to_16bits(self, value):
        '''
        converting array of 24bits back into 16 bit for SPI send register
        :return: array of 2 values by 16 bits each
        '''
        byte1 = (value >> 16) & 0xFFFF
        byte2 = value & 0xFFFF
        return [byte1, byte2]

    @micropython.native
    def _get_adc_val_from_res_val(self, res_Ohm):
        res_Ohm = range_check(res_Ohm, 0, 249900)
        Rw = 50  # wiper resistance, datasheet
        # Rab = 250000  # full scale resistance 250k -> in Ohm
        cnt = 1024 * (res_Ohm - Rw) / self.Rab
        cnt = int(round(cnt, 0))
        return cnt

    @micropython.native
    def _spi_write(self, command):
        self.cs.low()  # Select the Chip select
        self.spi.write(bytes(command))  # write buffer
        self.cs.high()  # Deselect the Chip select


