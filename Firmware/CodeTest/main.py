import sys
import uasyncio
import select


def main():
    poll_object = select.poll()
    poll_object.register(sys.stdin, 1)
    print("Welcome to the Simple CLI!")
    print("Type 'exit' to quit.")
    counter = 0
    while True:
        uasyncio.sleep(0.1)  # Simulate some v
        counter = counter +1
        if poll_object.poll(0):
            # read as character
            cmd = sys.stdin.readline(100)
            # print(bytearray(cmd.encode()))
            if cmd != "\n":  # Check if there's any data available to read
                cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
                # print(cmd_with_params)
                print(cmd_with_params, counter)
            sys.stdout.write(">")

if __name__ == "__main__":
    main()
