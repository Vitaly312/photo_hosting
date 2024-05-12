import json
import string
import random
from pathlib import Path
from datetime import date
from flask import request
from werkzeug.utils import secure_filename
from datetime import date, timedelta


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_CHARS = (string.ascii_uppercase + string.ascii_lowercase 
        + string.digits)

photo_folder = Path(__file__).parent / 'photo_storage'
print(photo_folder)
def generate_random_id(count: int = 20) -> str:
    text = [random.choice(ALLOWED_CHARS) for _ in range(count)]
    return ''.join(text)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

def delete_deprecated_photos():
    for folder in photo_folder.iterdir():
        if folder.is_file():
            continue
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

def save_photo(description: str | None, storage_time: int) -> list[str]:
    '''save photo in files, and return list of urls'''
    result = []
    for file in request.files.getlist("photo"):
        if not allowed_file(secure_filename(file.filename)):
            raise ValueError
    for file in request.files.getlist("photo"):
        filename = secure_filename(file.filename)
        uid = generate_random_id()
        new_storage = photo_folder / uid
        new_storage.mkdir(parents=True)
        file.save(new_storage / filename)
        with open(new_storage / "data.json", 'w+') as fp:
            destroy_at = date.today() + timedelta(days=storage_time)
            data = {
                "must_be_deleted_at": str(destroy_at),
                "description": description,
                "url": f"/photo/{uid}/{filename}"
                }
            json.dump(data, fp)
            result.append(f"/photo/{uid}/")
    return result
