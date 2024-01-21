# import machine
# import time
# from micropython import const
# from rp2 import PIO, asm_pio


def range_check(val, min, max):
    if val > max:
        # print(f"Wrong {val_name}: {val}. Max output should be less then {max} V")
        val = max
    if val < min:
        # print(f"Wrong {val_name}: {val}. Should be >= {min}")
        val = min
    return val


class AD9235_class:
    def __init__(self, spi=0, sck_pin=1, mosi_pin=2, miso_pin=3, cs_pin=4, daisy_chain=4):

        # Configure CS pin as an output
        # note 16 bit buffer as RP2040 support it
        # machine.SPI(0,
        #             baudrate=1_000_000,
        #             sck=machine.Pin(sck_pin),
        #             mosi=machine.Pin(mosi_pin),
        #             miso=machine.Pin(miso_pin),
        #             cs=machine.Pin(cs_pin),
        #             txbuf=0,
        #             rxbuf=0,
        #             polarity=0,
        #             phase=0,
        #             bits=16)
        #
        # self.cs = machine.Pin(cs_pin, machine.Pin.OUT)
        # # Initialize SPI
        # self.spi.init(baudrate=self.clk_freq, polarity=0, phase=0)

        self.ch = daisy_chain *2
        self.buf_set_r = [0] * self.ch  # buffer for setting resistor value in ADC counts
        self.buf_rd = [0] * self.ch  # buffer for reading current start of wiper position in ADC counts
        self.buf_cmd = [0] * self.ch  # buffer for SPI command
        self.buf_spi_tx = [0] * self.ch *2  # SPI transmit buffer

    # def read_adc(self):
    #     # Select the ADC
    #     self.cs.value(0)
    #
    #     # Send command to read ADC data
    #     command = bytes([0x01, 0x02, 0x03])  # Replace with the actual command bytes
    #     self.spi.write(command)
    #
    #     # Read data from ADC
    #     data = self.spi.read(2)  # Replace with the actual number of bytes to read
    #
    #     # Deselect the ADC
    #     self.cs.value(1)
    #
    #     # Process and return the ADC data
    #     adc_value = (data[0] << 8) | data[1]  # Replace with your data processing logic
    #     return adc_value
    # def query(self, cmd_array):
    # def set_rdaq(self, ch, val):
    def set_buffer(self, position, reg_val):
        '''
        :param position: postion of resistor. IC0 -> 0,1; IC1 ->2,3; IC3 -> 4,5; IC4 -> 6,7
        :param reg_val: register value from 0 to 1023
        :return: none
        '''
        reg_val = int(range_check(reg_val, 0, 1023))
        self.buf_set_r[position] = reg_val

    def test_buffer(self):
        self.__fill_cmd_buf()
        hex_array_1 = [hex(value) for value in self.buf_set_r]
        hex_array_2 = [hex(value) for value in self.buf_cmd]
        hex_array_3 = [hex(value) for value in self.buf_spi_tx]
        print(hex_array_1)
        print(hex_array_2)
        print(hex_array_3)


    def __fill_cmd_buf(self):
        '''
        trasform value buffer inti
        :return:
        '''
        cmd = []
        for index, value in enumerate(self.buf_set_r):
            if index % 2 == 0:
                ch = 1
            else:
                ch = 0
            cmd.append(self.__get_command("wrt",ch,value))
        self.buf_cmd = cmd
        cmd = []
        for item in self.buf_cmd:
            cmd.append(self.__convert_to_16bits(item))
        # make flat array from array of arrays
        flat_array = [item for array in cmd for item in array]
        self.buf_spi_tx = flat_array

    def __get_command(self, cmd="nop", ch=0, data=0):
        # cmd_nop = const(0x00)
        # cmd_wrt_rdac = const(0b10110000)  # cmd 11 datasheet
        # cmd_store_wiper_eemem = const(0b00100000)
        # cmd_rd_rdac = const(0b10100000)
        cmd_nop = 0x00
        cmd_wrt_rdac =0b10110000 # cmd 11 datasheet
        cmd_store_wiper_eemem = 0b00100000
        cmd_rd_rdac = 0b10100000
        data = int(range_check(data, 0, 1024))
        ch = int(range_check(ch,0,1))
        # set cmd then
        cmd_var = 0
        if cmd == "wrt":
            cmd_var = cmd_wrt_rdac
        elif cmd == "rd":
            cmd_var = cmd_rd_rdac
        elif cmd == "srt_wiper":
            cmd_var = cmd_store_wiper_eemem
        else:
            cmd_var = cmd_nop
        adc_value = (cmd_var << 16) | (ch << 16) | data
        return adc_value

    def __convert_to_8bits(self,value):
        '''
        converting array of 24bits back into 8 bit for SPI send register
        :return: array of 3 values by 8 bits each
        '''
        byte1 = (value >> 16) & 0xFF
        byte2 = (value >> 8) & 0xFF
        byte3 = value & 0xFF
        return [byte1, byte2, byte3]

    def __convert_to_16bits(self, value):
        '''
        converting array of 24bits back into 16 bit for SPI send register
        :return: array of 2 values by 16 bits each
        '''
        byte1 = (value >> 16) & 0xFFFF
        byte2 = value & 0xFFFF
        return [byte1, byte2]


