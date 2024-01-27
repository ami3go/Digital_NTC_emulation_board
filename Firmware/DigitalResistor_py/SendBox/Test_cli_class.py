import CLI_class

def turn_on_led(param, param2):
    # Custom action to turn on the LED based on the parameter
    print("Led On")


def turn_off_led(param, param2):
    # Custom action to turn off the LED based on the parameter
    print("Led Off")

cli = CLI_class.simplePyCLI(">")
cmd_help = "turning led on "
cli.add_command('led_on', turn_on_led, 2, cmd_help)  # Add a custom command "led_on" with the corresponding action
cmd_help = "turning led off "
cli.add_command('led_off', turn_off_led, 2, cmd_help)  # A
cmd_help = "print help"
cli.add_command('help_cmd', help, 1, cmd_help)  # A
while True:
    cmd  = input(">")
    if bool(cmd):  # Check if there's any data available to read
        cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
        # print(cmd_with_params)
        cli.process_command(cmd_with_params)  # Process the command