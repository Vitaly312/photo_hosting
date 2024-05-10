import json

from pathlib import Path
from datetime import date


photo_folder = Path(__file__).parent.parent / 'photo_storage'


def delete_deprecated_photos():
    for folder in photo_folder.iterdir():
        with open(folder / 'data.json', 'r') as fp:
            data = json.load(fp)
        if date.fromisoformat(data['must_be_deleted_at']) < date.today():
            for file in folder.iterdir():
                try:
                    file.unlink()
                except:
                    print("Warning, deprecated photo was skipped because of a PermissionError")
                    return
            folder.rmdir()

def get_photo_urls(photo_dir: Path) -> list[str]:
    return [f'/photo/{photo_dir.name}/{file.name}' 
            for file in photo_dir.iterdir()
            if file.is_file() and file.suffix != '.json']
