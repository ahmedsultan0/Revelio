from magic.image_indexer import process_images
from revilio import global_index
from magic.console_utils import console


def index():
    folder_to_index = console.input("Enter folder to index images: ").strip()
    images_data = process_images(folder_to_index)
    global_index = images_data