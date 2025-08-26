from concurrent.futures import ThreadPoolExecutor, as_completed
from magic.config import EXCLUDED_DIRS, EXCLUDED_SUB_DIRS, IMAGE_EXTENSIONS
from pathlib import Path
from magic.console_utils import console


def is_excluded(path: Path):
    """Check if a path is in excluded directories or is inside a famous hidden directory."""
    abs_path = path.resolve()

    if any(str(abs_path).startswith(str(Path(ex).resolve())) for ex in EXCLUDED_DIRS):
        return True

    if any(str(Path(ex).resolve()) in str(abs_path) for ex in EXCLUDED_SUB_DIRS):
        return True
    
    return False

def index_images(start_paths, max_paths=30000):
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
        "size": defaultdict(list),
        "type": defaultdict(list),
        "name": []
    }

    indexed_images = list(index_images(start_path))
    successful_count = 0

    def get_image_info(path):
        try:
            size_mb = round(path.stat().st_size / 1024 / 1024, 2)
            return {
                "path": str(path),
                "name": path.name,
                "size_mb": size_mb,
                "type": path.suffix.lower().lstrip('.')
            }
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(get_image_info, path): path for path in indexed_images}
        for future in as_completed(future_to_path):
            data = future.result()
            if data:
                cat = size_category(data['size_mb'])
                images_by['size'][cat].append(data)
                images_by['type'][data['type']].append(data)
                images_by['name'].append(data["name"])
                successful_count += 1  
    return images_by
