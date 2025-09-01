import os
from magic.config import BL, LB
from rich.console import Console
from rich.text import Text
from urllib.parse import quote

console = Console()

default_line_start = f"[{BL}][ ! ] "

general_text_format = lambda message, type=None: (
    f"\n{default_line_start}[{LB}]{message}" if type == "info" else 
    f"\n{default_line_start}[red]{message}[/red]" if type == "error" else 
    f"{default_line_start}[green]{message}[/green]" if type == "success" else 
    f"{default_line_start}[{LB}]{message}" if type == "loading" else 
    f"\n[{BL}][ + ] [{LB}]{message}"
)

def file_info_format(info):
    text = Text()

    text.append(f"{info['id'][:8]:<10}", style="white")
    text.append(f"{info['name'][:40]:<40}", style=LB)
    text.append(f"{info['size_mb']:>6.2f}MBs ", style="green")
    path_url = "file://" + quote(info['path'])
    text.append("(open)", style=f"link {path_url} {BL}")
    return text


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
