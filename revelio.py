from time import sleep
from magic.utils.console_utils import clear, welcome
from magic.workflow.menu import execute_option, option_text
from magic.utils.console_utils import console, general_text_format
from magic.inventory import db_connection
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

global_index = {
    "records": {},
    "size": {"S": [], "M": [], "L": [], "XL": []},
    "type": {},
    "name": [],
    "name_to_id": {},
}

def main(clear_screen=True):
    if clear_screen:
        clear()
        welcome()
    else:
        sleep(1.25)
    console.print(option_text())

    if(len(global_index) == 0):
        db_connection.load_all_from_table()

    try:
        opt = int(console.input(general_text_format("Select Option : ")))
        execute_option(opt)
    except ValueError:
        console.print(general_text_format('Please input number', "info"))
        main()


if __name__ == '__main__':
    try:
        db_connection.load_all_from_table()
        main()
    except KeyboardInterrupt:
        console.print(general_text_format("Mischief Managed! 🪄", "info"))
        exit()