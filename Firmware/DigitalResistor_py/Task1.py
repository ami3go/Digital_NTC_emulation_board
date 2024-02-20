import AD5235 as dig_res
import select
import sys
import simplePyCLI as cli_class
import uasyncio
import utils as ut


async def cli_task():
    cli = cli_class.simplePyCLI(">")
    dev = dig_res.AD5235_class()
    # # setup poll to read USB port
    poll_object = select.poll()
    poll_object.register(sys.stdin,1)


    def set_reg(ch_num, val):
        if ut.is_digit(ch_num) and ut.is_digit(val):
            dev.set_raw_val(int(ch_num), int(val))
            print(f"ch_num: {int(ch_num)}, reg_val: {int(val)}")

    def set_res(ch_num, val):
        if ut.is_digit(ch_num) and ut.is_digit(val):
            dev.set_Ohm_val(int(ch_num), int(val))
            print(f"ch_num: {int(ch_num)}, res_val: {int(val)}")

    def write_to_dev():
        dev.write_resistance()

    def set_reg_all(val):
        if ut.is_digit(val):
            for i in range(8):
                dev.set_raw_val(i, int(val))
            dev.write_resistance()

    def set_res_all(val):
        if ut.is_digit(val):
            for i in range(8):
                dev.set_Ohm_val(i, int(val))
            dev.write_resistance()

    def get_res():
        print(dev.get_res_buffer)

    def store_wiper():
        dev.store_wiper_to_eemem()

    def restore_wiper():
        dev.restore_wiper()

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

    cmd_str = "store_wiper"
    cmd_action = store_wiper
    n_params = 0
    cmd_help = "Save current wiper position to internal EEMEM"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    cmd_str = "restore_wiper"
    cmd_action = restore_wiper
    n_params = 0
    cmd_help = "Save current wiper position to internal EEMEM"
    cli.add_command(cmd_str, cmd_action, n_params, cmd_help)

    delay = 0.05
    sys.stdout.write(">")
    while True:
        await uasyncio.sleep(delay)  # Simulate some v
        if poll_object.poll(0):
        #read as character
            cmd = sys.stdin.readline(100)
            # print(bytearray(cmd.encode()))
            if cmd != "\n": # Check if there's any data available to read
                cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
                # print(cmd_with_params)
                cli.process_command(cmd_with_params)  # Process the command
                sys.stdout.write(">")