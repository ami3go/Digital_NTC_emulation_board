# https://www.waveshare.com/wiki/RP2040-Zero
# http://staff.ltam.lu/feljc/electronics/uPython/Pico_communication.pdf
# import libs.AD5235.AD5235m as dig_res
# import libs.LED.Led
import simplePyCLI as cli_class
import uasyncio
import time
from machine import Pin
import rp2
def cli_task():
    cli = cli_class.simplePyCLI(">")
    # dev = dig_res.AD5235_class()
    def set_reg(ch_num, reg_val):
        # Custom action to turn on the LED based on the parameter
        print(f"ch_num: {ch_num}, reg_val: {reg_val}")

    def set_res(ch_num, val):
        # Custom action to turn on the LED based on the parameter
        print(f"ch_num: {ch_num}, reg_val: {val}")

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
    delay = 0.05
    while True:
        await uasyncio.sleep(delay)  # Simulate some v
        cmd = input(">")
        if bool(cmd):  # Check if there's any data available to read
            cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
            # print(cmd_with_params)
            cli.process_command(cmd_with_params)  # Process the command

async def main():
    # queue = asyncio.Queue()
    cli_tsk = uasyncio.create_task(cli_task())
    await cli_tsk

uasyncio.run(main())