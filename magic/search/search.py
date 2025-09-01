import re
from magic.config import BL, LB
from magic.console_utils import console, general_text_format, file_info_format
from magic.menu import option_text
from revelio import global_index
from .options import search_options

def search_input(prompt, error_msg, key, transform=lambda x: x, filter_fn=None):
    """Generic search handler for global_index lookups."""
    try:
        opt = console.input(general_text_format(prompt)).strip()
        opt = transform(opt)


        if not opt:
            console.print(general_text_format(error_msg))
            return
        
        pattern = None
        
        if key == "regex":
            pattern = re.compile(opt.replace("*", ".*").replace("?", "."), re.IGNORECASE)

        data = global_index.get(key if key != "regex" else "name", {} if key not in ["name", "regex"] else [])
        images_hashes = data.get(opt, []) if key not in ["name", "regex"] else [
            global_index["name_to_id"][name] for name in data if filter_fn(opt, name, pattern)
        ]

        if not images_hashes:
            console.print(general_text_format(f"No images found for {key}: {opt}", "info"))

        for img_hash in images_hashes:
            console.print(file_info_format(global_index["records"][img_hash]))

    except Exception as e:
        console.print(general_text_format(f"Error while searching images.", "error"))


def search_size():
    search_input(
        prompt="Select a size (S/M/L):",
        error_msg="Invalid option. Please enter S, M, or L.",
        key="size",
        transform=lambda x: x.upper()
    )


def search_type():
    search_input(
        prompt="Select a type (jpg/png/gif):",
        error_msg="Invalid option. Please enter (jpg/png/gif).",
        key="type",
        transform=lambda x: x.lower()
    )


def search_name():
    search_input(
        prompt="Enter a name: ",
        error_msg="Invalid option. Please enter a name.",
        key="name",
        transform=lambda x: x.lower(),
        filter_fn=lambda opt, name, pattern: opt in name.lower()
    )


def search_regex():
    search_input(
        prompt="Enter a regex: ",
        error_msg="Invalid option. Please enter a correct regex.",
        key="regex",
        transform=lambda x: x.lower(),
        filter_fn=lambda opt, name, pattern: pattern.search(name)
    )


def search():

    if(len(global_index["name"]) == 0):
        console.print(general_text_format("No images scanned yet. Please scan first with option 1.", "info"))
        return

    console.print(option_text(search_options))
    opt = console.input(general_text_format("Select a search operation (S/N/T/R): ", "info")).strip().upper()

    func_map = {
        'S': search_size,
        'N': search_name,
        'T': search_type,
        'R': search_regex
    }

    func = func_map.get(opt)
    if func:
        func()
    else:
        console.print(general_text_format("Invalid option. Please enter S, N, T or R.", "info"))
