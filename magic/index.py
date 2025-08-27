from magic.config import BL, LB
from magic.image_indexer import process_images
from magic.console_utils import console, general_text_format
import itertools, threading, time
import revelio

def loading_spinner(stop_event):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        console.print(general_text_format(f"Indexing images... [white]{next(spinner)}", "loading"), end="\r")

        time.sleep(0.1)


def index():
    folder_to_index = console.input(general_text_format("Enter a folder to scan the images: ")).strip()
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner_thread.start()

    number_of_images_processed, number_of_images_already_processed = process_images(folder_to_index)

    stop_event.set()
    spinner_thread.join()
    if number_of_images_already_processed > 0:
        console.print(general_text_format(f"Re-indexing {number_of_images_already_processed} old images is complete!", "success"))
    console.print(general_text_format(f"Indexing {number_of_images_processed} new images is complete!", "success"))
    
