import os
from magic.config import BL, LB
from rich.console import Console

console = Console()

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')


def welcome(): 
    clear()

    art_banner = f"""\n
         ███████████                                 ████   ███          
        ░░███░░░░░███                               ░░███  ░░░           
        ░███    ░███   ██████  █████ █████  ██████  ░███  ████   ██████ 
        ░██████████   ███░░███░░███ ░░███  ███░░███ ░███ ░░███  ███░░███
        ░███░░░░░███ ░███████  ░███  ░███ ░███████  ░███  ░███ ░███ ░███
        ░███    ░███ ░███░░░   ░░███ ███  ░███░░░   ░███  ░███ ░███ ░███
        █████   █████░░██████   ░░█████   ░░██████  █████ █████░░██████ 
        ░░░░░   ░░░░░  ░░░░░░     ░░░░░     ░░░░░░  ░░░░░ ░░░░░  ░░░░░░         
        \n
        [{LB}]Revelio is a spill to find any image file in your system[/]\n
        [{LB}][ + ]  C O D E D   B Y  A H M E D  [ + ][/]    
    """

    art_banner = (
        art_banner.replace("█", f"[{LB}]█[/]")
                  .replace("░", f"[{BL}]░[/]")
    )

    console.print(art_banner, end="\n")
