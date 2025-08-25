from time import sleep
from magic.config import BL, LB
from magic.console_utils import clear, welcome
from magic.menu import execute_option, option_text
from magic.console_utils import console

global_index = {}

def main(clear_screen=True):
    if clear_screen:
        clear()
        welcome()
    else:
        sleep(1.5)
    console.print(option_text())
    try:
        opt = int(console.input(f"\n[{BL}][ + ] [{LB}]Select Option : [/]"))
        execute_option(opt)
    except ValueError:
        console.print(f'\n[{BL}][ ! ] [{LB}]Please input number [/]')
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{BL}][ ! ] [{LB}]Mischief Managed! 🪄")
        exit()