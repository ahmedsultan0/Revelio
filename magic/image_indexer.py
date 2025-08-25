from concurrent.futures import ThreadPoolExecutor, as_completed
from magic.config import EXCLUDED_DIRS, IMAGE_EXTENSIONS
from pathlib import Path
from magic.console_utils import console


def is_excluded(path: Path):
    """Check if a path is in excluded directories."""
    abs_path = path.resolve()
    return any(str(abs_path).startswith(str(Path(ex).resolve())) for ex in EXCLUDED_DIRS)

def index_images(start_paths, max_paths=300):
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

def size_category(size_kb):
    """Classify size in KB into Small / Medium / Large"""
    if size_kb < 500:
        return "Small"
    elif size_kb < 2000:
        return "Medium"
    else:
        return "Large"

def process_images(start_path, max_workers=4):
    """
    Index and classify images in parallel by size only.
    Returns a dictionary with key 'size' mapping category -> list of image info.
    """
    from collections import defaultdict

    images_by = {
        "size": defaultdict(list)
    }

    indexed_images = list(index_images(start_path))
    successful_count = 0

    def get_image_info(path):
        try:
            size_kb = round(path.stat().st_size / 1024, 2)
            return {
                "path": str(path),
                "size_kb": size_kb
            }
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(get_image_info, path): path for path in indexed_images}
        for future in as_completed(future_to_path):
            data = future.result()
            if data:
                cat = size_category(data['size_kb'])
                images_by['size'][cat].append(data)
                successful_count += 1  
                console.print(f"successfully processed: {successful_count}", end='\r')
    return images_by
