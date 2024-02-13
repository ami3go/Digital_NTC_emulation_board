# https://www.waveshare.com/wiki/RP2040-Zero
# http://staff.ltam.lu/feljc/electronics/uPython/Pico_communication.pdf
import AD5235m as dig_res
# import libs.LED.Led
import simplePyCLI as cli_class
import Led
import uasyncio
import utils as ut
import time
from machine import Pin
import rp2
import urandom

async def cli_task():
    cli = cli_class.simplePyCLI(">")
    dev = dig_res.AD5235_class()
    def set_reg(ch_num, val):
        if ut.is_digit(ch_num) and ut.is_digit(val):
            dev.set_raw_val(int(ch_num), int(val))
            print(f"ch_num: {int(ch_num)}, reg_val: {int(val)}")

    def set_res(ch_num, val):
        if ut.is_digit(ch_num) and ut.is_digit(val):
            dev.set_Ohm_val(int(ch_num), int(val))
            print(f"ch_num: {int(ch_num)}, res_val: {int(val)}")

    def write_to_dev():
        dev.write_to_dev()

    def set_reg_all(val):
        if ut.is_digit(val):
            for i in range(8):
                dev.set_raw_val(i, int(val))
            dev.write_to_dev()

    def set_res_all(val):
        if ut.is_digit(val):
            for i in range(8):
                dev.set_Ohm_val(i, int(val))
            dev.write_to_dev()

    def get_res():
        print(dev.get_res_buffer)

    cmd_str = "set_reg"
    cmd_action = set_reg
    n_params = 2
    cmd_help = "Set register value: 'set_reg 0 1023'"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "set_res"
    cmd_action = set_res
    n_params = 2
    cmd_help = "Set register value: 'set_reg 0 250k'"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "write"
    cmd_action = write_to_dev
    n_params = 0
    cmd_help = "Write resistance value from software buffer to IC"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "set_reg_all"
    cmd_action = set_reg_all
    n_params = 1
    cmd_help = "Set all 8 channels same value and write it to IC"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "set_res_all"
    cmd_action = set_res_all
    n_params = 1
    cmd_help = "Set all 8 channels same value and write it to IC"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "get_res"
    cmd_action = get_res
    n_params = 0
    cmd_help = "Get current state of resistance buffer"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    delay = 0.05
    while True:
        await uasyncio.sleep(delay)  # Simulate some v
        cmd = input(">")
        if bool(cmd):  # Check if there's any data available to read
            cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
            # print(cmd_with_params)
            cli.process_command(cmd_with_params)  # Process the command
async def led_task():
    led = Led.LEDController(16,1)
    delay = 0.01
    r = 0
    g = 0
    b = 255
    while True:
        led.set_color(0, (r, g, b))
        await uasyncio.sleep(delay)  # Simulate some v
        led.clear()
        await uasyncio.sleep(delay)  # Simulate some v
        r = urandom.getrandbits(8)
        g = urandom.getrandbits(8)
        b = urandom.getrandbits(8)



async def main():
    # queue = asyncio.Queue()
    cli_tsk = uasyncio.create_task(cli_task())
    led_tsk = uasyncio.create_task(led_task())
    await cli_tsk
    await led_tsk

uasyncio.run(main())