import asyncio


# Define a coroutine to control <link>WS2812B LEDs</link>
async def task_1(color_queue):
    delay = 1
    while True:
        # Set LED color to red
        print("Task1")
        await asyncio.sleep(delay)  # Delay for 0.5 seconds
        array = ["red", "green", "blue"]
        for color in array:

            await color_queue.put(color)
        await asyncio.sleep(delay)  # Simulate some v
        # # Set LED color to green
        # led_controller.set_color(0,(0, 255, 0))
        # await asyncio.sleep(delay)  # Delay for 0.5 seconds

        # # Set LED color to blue
        # led_controller.set_color(0,(0, 0, 255))
        # await asyncio.sleep(delay)  # Delay for 0.5 seconds


async def task_2(color_queue):
          while True:
            # # Set LED color to red
            # led_controller.set_color(0,(255, 0, 0))
            # await asyncio.sleep(delay)  # Delay for 0.5 seconds

            # Set LED color to green

            message = await color_queue.get()
            print("task2", message)
            color_queue.task_done()
            # await asyncio.sleep(delay)  # Delay for 0.5 seconds

            # # Set LED color to blue
            # led_controller.set_color(0,(0, 0, 255))
            # await asyncio.sleep(delay)  # Delay for 0.5 seconds


# # Function to set <link>WS2812B</link> color (replace this with your actual LED control function)
# def set_ws2812b_color(red, green, blue):
#     print(f"Setting <link>WS2812B</link> color to R:{red}, G:{green}, B:{blue}")

# Run the asyncio event loop with the LED control coroutine
async def main():
    color_queue = asyncio.Queue()
    task1 = asyncio.create_task(task_1(color_queue))
    task2 = asyncio.create_task(task_2(color_queue))
    await asyncio.gather(task1, task2)


asyncio.run(main())