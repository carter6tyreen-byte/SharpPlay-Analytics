import os
import shutil
from pathlib import Path

def migrate():
    # Define paths
    root = Path(".")
    src_dir = root / "src"
    consolidator_old = root / "data" / "data_consolidator.py"
    consolidator_new = src_dir / "data_consolidator.py"

    # 1. Create src directory
    if not src_dir.exists():
        src_dir.mkdir()
        print(f"Created directory: {src_dir}")

    # 2. Add __init__.py
    init_file = src_dir / "__init__.py"
    init_file.touch()
    print(f"Created file: {init_file}")

    # 3. Move the file
    if consolidator_old.exists():
        shutil.move(str(consolidator_old), str(consolidator_new))
        print(f"Moved {consolidator_old} to {consolidator_new}")
    else:
        print(f"File {consolidator_old} not found. Check your paths.")

if __name__ == "__main__":
    migrate()
