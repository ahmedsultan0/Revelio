from magic.config import BL, LB
from magic.console_utils import console
from magic.menu import option_text
from magic.constants import general_text_format
from revelio import global_index
from .options import search_options


def search_input(prompt, error_msg, key, transform=lambda x: x, filter_fn=None):
    """Generic search handler for global_index lookups."""
    opt = console.input(general_text_format(prompt)).strip()
    opt = transform(opt)

    if not opt:
        console.print(general_text_format(error_msg))
        return

    data = global_index.get(key, {} if key != "name" else [])
    images = data.get(opt, []) if key != "name" else [
        name for name in data if filter_fn and filter_fn(opt, name)
    ]

    if images:
        for img in images:
            print(img)
    else:
        console.print(general_text_format("No images found for {key}: {opt}", "info"))


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
        filter_fn=lambda opt, name: opt in name.lower()
    )


def search():
    console.print(option_text(search_options))
    opt = console.input(general_text_format("Select a search operation (S/N/T): ", "info")).strip().upper()

    func_map = {
        'S': search_size,
        'N': search_name,
        'T': search_type
    }

    func = func_map.get(opt)
    if func:
        func()
    else:
        console.print(general_text_format("Invalid option. Please enter S, N, or T.", "info"))
