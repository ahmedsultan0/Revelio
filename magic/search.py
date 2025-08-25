from magic.config import BL, LB
from magic.console_utils import console
from revilio import global_index

def search():
    opt = console.input(f"\n[{BL}][ + ] [{LB}]Select a size (S/M/L): [/]").strip().upper()
    if not opt:
        console.print(f"[{BL}][ ! ] [{LB}]Invalid option. Please enter S, M, or L.[/]")
        return
    images = global_index.get('size', {}).get(opt, [])
    if images:
        for img in images:
            print(img)
    else:
        console.print(f"[{BL}][ ! ] [{LB}]No images found for size: {opt}[/]")