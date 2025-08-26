from time import sleep
from magic.config import BL, LB
from magic.console_utils import clear, welcome
from magic.menu import execute_option, option_text
from magic.console_utils import console
from magic.constants import general_text_format

global_index = {}

def main(clear_screen=True):
    if clear_screen:
        clear()
        welcome()
    else:
        sleep(1.5)
    console.print(option_text())
    try:
        opt = int(console.input(general_text_format("Select Option : ")))
        execute_option(opt)
    except ValueError:
        console.print(general_text_format('Please input number', "info"))
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print(general_text_format("Mischief Managed! 🪄", "info"))
        exit()