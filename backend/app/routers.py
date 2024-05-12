import json
from pathlib import Path
from flask import render_template, request, redirect, send_file, Response, flash

from app.forms import PhotoUploadForm
from app import app
from app.utils import save_photo


photo_folder = Path(__file__).parent.parent / 'photo_storage'

@app.route('/', methods=['POST', "GET"])
def hello_world():
    form = PhotoUploadForm()
    if form.validate_on_submit() and request.files:
        try:
            photo_urls = save_photo(form.description.data, form.storage_time.data)
        except ValueError:
            flash("Однин из файлов имеет недопустимый формат")
            return render_template('index.html', form=form)
        else:
            return redirect(f"/success_upload/?photo_id={','.join(photo_urls)}")
    else:
        return render_template('index.html', form=form)


@app.route("/photo/<photo_dir>/")
def get_photo_folder(photo_dir: str):
    path = photo_folder / photo_dir
    if path.exists():
        with open(path / 'data.json', 'r') as fp:
            photo_info = json.load(fp)
        #photo_info['photo_urls'] = get_photo_urls(path)
        photo_info['has_photo'] = True
        
    else:
        photo_info = {
            'url': 'static/default_photo.jpg',
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
                           photo_urls = [uri
                                        for uri in request.args.get("photo_id").split(",")])
