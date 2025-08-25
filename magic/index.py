from magic.image_indexer import process_images
import revelio
from magic.console_utils import console

def index():
    folder_to_index = console.input("Enter folder to index images: ").strip()
    images_data = process_images(folder_to_index)
    revelio.global_index.clear()
    revelio.global_index.update(images_data)