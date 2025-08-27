import os
from magic.config import BL, LB
from magic.constants import default_line_start
from rich.console import Console

console = Console()

general_text_format = lambda message, type=None: (
    f"\n{default_line_start}[{LB}]{message}" if type == "info" else 
    f"\n{default_line_start}[red]{message}[/red]" if type == "error" else 
    f"{default_line_start}[green]{message}[/green]" if type == "success" else 
    f"{default_line_start}[{LB}]{message}" if type == "loading" else 
    f"\n[{BL}][ + ] [{LB}]{message}"
)

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
        [{LB}]Revelio is a spell to find any image file in your system[/]\n
        [{LB}][ + ]  C O D E D   B Y  A H M E D  [ + ][/]    
    """

    art_banner = (
        art_banner.replace("█", f"[{LB}]█[/]")
                  .replace("░", f"[{BL}]░[/]")
    )

    console.print(art_banner, end="\n")
