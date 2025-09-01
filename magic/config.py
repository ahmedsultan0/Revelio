BL = "#192BC2"
LB = "#57B2FF"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".dib", ".tif", ".tiff", 
                    ".webp", ".jpe", ".jfif", ".jfi", ".heic", ".heif", ".avif"}

# OS Folders to exclude
EXCLUDED_DIRS = [
    "/System", "/Library", "/usr", "/bin", "/sbin", "/opt", "/Applications", "/private/var" # macOS/Linux
    "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"  # Windows
]

EXCLUDED_SUB_DIRS = [
    "/.npm", "/.gradle", "/.npm", "/.vscode", "/.rbenv", "/node_modules"
]

SIZE_CATEGORIES_SPLIT = {"S": 0.5, "M": 2, "L": 10, "XL": float('inf')}  