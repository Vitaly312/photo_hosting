import string
import random
import json
from pathlib import Path
from flask import render_template, request, redirect, send_file, Response, flash
from werkzeug.utils import secure_filename
from datetime import date, timedelta

from app.forms import PhotoUploadForm
from app import app
from app.utils import get_photo_urls



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_CHARS = (string.ascii_uppercase + string.ascii_lowercase 
        + string.digits)

photo_folder = Path(__file__).parent.parent / 'photo_storage'

def generate_random_id(count: int = 20) -> str:
    text = [random.choice(ALLOWED_CHARS) for _ in range(count)]
    return ''.join(text)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', "GET"])
def hello_world():
    form = PhotoUploadForm()
    if form.validate_on_submit() and request.files:
        uid = generate_random_id()
        new_storage = photo_folder / uid
        new_storage.mkdir(parents=True)
        for file_id, file in enumerate(request.files.getlist('photo')):
            filename = secure_filename(file.filename)
            if not allowed_file(filename):
               flash("Однин из файлов имеет недопустимый формат")
               return render_template('index.html', form=form)
            file.save(str(new_storage / str(file_id)) + '.' 
                      + filename.split('.')[-1])
            
        with open(new_storage / "data.json", 'w+') as fp:
            destroy_at = date.today() + timedelta(days=form.storage_time.data)
            data = {
                "must_be_deleted_at": str(destroy_at),
                "description": form.description.data

                }
            json.dump(data, fp)

        return redirect(f"/success_upload/?photo_id={uid}")
    else:
        return render_template('index.html', form=form)


@app.route("/photo/<photo_dir>/")
def get_photo_folder(photo_dir: str):
    path = photo_folder / photo_dir
    if path.exists():
        with open(path / 'data.json', 'r') as fp:
            photo_info = json.load(fp)
        photo_info['photo_urls'] = get_photo_urls(path)
        photo_info['has_photo'] = True
        
    else:
        photo_info = {
            'photo_urls': ['static/default_photo.jpg'],
            'has_photo': False
        }
    return render_template("photo_view.html", photo_info = photo_info)

@app.route("/photo/<photo_dir>/<photo_id>")
def get_photo(photo_dir: str, photo_id: str):
    path = photo_folder / photo_dir / photo_id
    if not path.exists():
        return Response(status=404)
    return send_file(str(path))

@app.route('/success_upload/')
def success_download():
    return render_template('success_download.html', 
                           uri = f'/photo/{request.args.get("photo_id")}/')