from magic.config import BL, LB
from magic.image_indexer import process_images
from magic.console_utils import console
from magic.constants import general_text_format
import itertools, threading, time
import revelio

def loading_spinner(stop_event):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        console.print(general_text_format(f"Indexing images... [white]{next(spinner)}", "loading"), end="\r")

        time.sleep(0.1)


def index():
    folder_to_index = console.input(general_text_format("Enter folder to index images: ")).strip()
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner_thread.start()

    images_data = process_images(folder_to_index)

    # Update global index
    revelio.global_index.clear()
    revelio.global_index.update(images_data)

    stop_event.set()
    spinner_thread.join()

    console.print(general_text_format(f"Indexing {len(images_data['name'])} images is complete!", "success"))
    
