import itertools, threading, sys, time
from magic.config import BL, LB
from magic.image_indexer import process_images
import revelio
from magic.console_utils import console

def loading_spinner(stop_event):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        console.print(f"[{BL}][ + ] [{LB}]Indexing images... [white]{next(spinner)}", end="\r")
        time.sleep(0.1)


def index():
    folder_to_index = console.input("Enter folder to index images: ").strip()
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner_thread.start()

    images_data = process_images(folder_to_index)

    # Update global index
    revelio.global_index.clear()
    revelio.global_index.update(images_data)

    stop_event.set()
    spinner_thread.join()

    console.print(f"\n[{BL}][ + ] [green]Indexing {len(images_data['name'])} images is complete![/green]")
    
