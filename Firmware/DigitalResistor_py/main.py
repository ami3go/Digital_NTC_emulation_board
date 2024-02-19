# https://www.waveshare.com/wiki/RP2040-Zero
# http://staff.ltam.lu/feljc/electronics/uPython/Pico_communication.pdf
# # https://www.waveshare.com/wiki/RP2040-Zero
# # http://staff.ltam.lu/feljc/electronics/uPython/Pico_communication.pdf
import machine

import AD5235m as dig_res
import select
import sys
import simplePyCLI as cli_class
import Led
import uasyncio
import utils as ut
import time
from machine import Pin
import rp2
import urandom
import Task1




async def led_task():
    led = Led.LEDController(16,1)
    delay = 1
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
    cli_tsk = uasyncio.create_task(Task1.cli_task())
    led_tsk = uasyncio.create_task(led_task())
    await cli_tsk
    await led_tsk

uasyncio.run(main())

