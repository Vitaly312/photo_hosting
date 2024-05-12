from app import app
from flask import request, jsonify
from functools import wraps
from enum import Enum
from app.utils import save_photo


class UploadError(Enum):
    bad_api_key = 'Incorrect API key'
    bad_storage_time = "Incorrect storage time, integer value must be between 1 and 90"
    param_skipped = "You must send file and storage_time"
    too_long_description = "Description must be less than 1000 chars"
    bad_file = "Incorrect file type, file must be .jpg, .png or .jpeg"


def api_auth_required(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if request.headers['Api-Key'] == app.config['API_ACCESS_TOKEN']:
            return f(*args, **kwargs)
        else:
            return jsonify({'success': False, 'error': UploadError.bad_api_key}), 400
    return _wrapper


def serialize(body: dict) -> tuple[str, int] | dict[str, str]:
    print(body)

@app.route("/api/upload/", methods=['POST'])
@api_auth_required
def api_upload():
    print(request.form)
    body = request.form or {}
    if 'storage_time' not in body or not request.files:
        return jsonify({'success': False, 'error': UploadError.param_skipped.value}), 400
    try:
        storage_time = int(body['storage_time'])
    except ValueError:
        return jsonify({'success': False, 'error': UploadError.bad_storage_time.value}), 400
    if not (storage_time >= 1 and storage_time <= 90):
        return jsonify({'success': False, 'error': UploadError.bad_storage_time.value}), 400
    if len(body.get("description", "")) > 1000:
        return jsonify({'success': False, 'error': UploadError.too_long_description.value}), 400


    try:
        urls = save_photo(body.get('description', None), storage_time)
    except ValueError:
        return jsonify({'success': False, 'error': UploadError.bad_file.value}), 400
    else:
        return jsonify({"success": True, 'urls': urls}), 200
        