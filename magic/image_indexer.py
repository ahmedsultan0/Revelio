from concurrent.futures import ThreadPoolExecutor, as_completed
from magic.config import EXCLUDED_DIRS, EXCLUDED_SUB_DIRS, IMAGE_EXTENSIONS
from pathlib import Path
from magic.console_utils import console
from magic.inventory.db_connection import sync_dictionary_with_db
from magic.constants import general_text_format
import revelio

def is_excluded(path: Path):
    """Check if a path is in excluded directories or is inside a famous hidden directory."""
    abs_path = path.resolve()

    if any(str(abs_path).startswith(str(Path(ex).resolve())) for ex in EXCLUDED_DIRS):
        return True

    if any(str(Path(ex).resolve()) in str(abs_path) for ex in EXCLUDED_SUB_DIRS):
        return True
    
    return False

def index_images(start_paths, max_paths=1000000):
    """Yield image paths recursively from start_paths, excluding system folders."""
    if isinstance(start_paths, str):
        start_paths = [start_paths]

    paths = 0

    for start in start_paths:
        start_path = Path(start).resolve()
        for path in start_path.rglob("*"):
            if paths >= max_paths:
                return 
            if path.suffix.lower() in IMAGE_EXTENSIONS and not is_excluded(path):
                paths += 1
                yield path

def size_category(size_mb):
    """Classify size in KB into Small / Medium / Large"""
    if size_mb < 0.5:
        return "S"
    elif size_mb < 2:
        return "M"
    else:
        return "L"

def process_images(start_path, max_workers=4):
    """
    Index and classify images in parallel by size only.
    Returns a dictionary with key 'size' mapping category -> list of image info.
    """
    from collections import defaultdict

    images_by = {
        "size": revelio.global_index["size"],
        "type": revelio.global_index["type"],
        "name": revelio.global_index["name"],
        "path": revelio.global_index["path"],
    }

    indexed_images = list(index_images(start_path))
    successful_count = 0
    already_indexed_count = 0

    def get_image_info(path):
        try:
            size_mb = round(path.stat().st_size / 1024 / 1024, 2)
            return {
                "path": str(path),
                "name": path.name,
                "size_mb": size_mb,
                "file_type": path.suffix.lower().lstrip('.')
            }
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(get_image_info, path): path for path in indexed_images}
        for future in as_completed(future_to_path):
            data = future.result()
            if data and data["path"] not in images_by['path']:
                cat = size_category(data['size_mb'])
                images_by['size'][cat].append(data)
                images_by['type'].get(data['file_type'], []).append(data)
                images_by['name'].append(data["name"])
                successful_count += 1 
            else:
                already_indexed_count += 1
    
    # try:
    sync_dictionary_with_db(images_by['size']['S'] + images_by['size']['M'] + images_by['size']['L'], ['path', 'name',  'size_mb', 'file_type'], 'files')
    revelio.global_index.update(images_by)
    # except Exception as e:
    #     console.print(general_text_format(f"Error syncing with DB sync", "error"))
    #     print(e) #remove later

    return successful_count, already_indexed_count
