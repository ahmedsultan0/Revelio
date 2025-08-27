from magic.config import BL, LB

default_line_start = f"[{BL}][ ! ] "

general_text_format = lambda message, type=None: (
    f"\n{default_line_start}[{LB}]{message}" if type == "info" else 
    f"\n{default_line_start}[red]{message}[/red]" if type == "error" else 
    f"{default_line_start}[green]{message}[/green]" if type == "success" else 
    f"{default_line_start}[{LB}]{message}" if type == "loading" else 
    f"\n[{BL}][ + ] [{LB}]{message}"
)