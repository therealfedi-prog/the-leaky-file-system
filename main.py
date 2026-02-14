import hashlib
import os
import time
import json
from datetime import datetime, timedelta

def calculate_file(filepath):
    sha256_hash = hashlib.sha256()
    f = open (filepath, 'rb')
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def valid_extension(filename):
    allowed = ['jpg', 'jpeg', 'png', 'gif', 'webp']

    if '.' in filename:
        extension = filename[filename.find("."):].lower()
        return extension in allowed
    return False

def valid_size(filename):
    max_vol = 5 * 1024 * 1024
    return os.path.getsize(filename) <= max_vol

def cleanup_old_files(filename):
    os.listdir(filename)
    creation_time = os.path.getctime(filename)
    daytime = 24*60*60
    current_time = time.time()
    if current_time - creation_time > daytime:
        os.remove(filename)

def save_file_metadata(file_hash, original_name, file_size, metadata_file='files.json'):
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

    file_info = {
        'hash': file_hash,
        'original_name': original_name,
        'size': file_size,
        'uploaded_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
    }
    metadata[file_hash] = file_info

    f = open(metadata_file, 'w')
    json.dump(metadata, f)

def is_duplicate(file_hash, metadata_file='files.json'):
    if not os.path.exists(metadata_file):
        return False

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    if file_hash in metadata:
        return True
    else:
        return False

#main code here :))))

def handle_file_upload(file_path, original_filename):
    if not valid_extension(original_filename):
        return {
            'success': False,
            'message': 'Invalid file type. Only JPG, PNG, GIF, WEBP allowed.'
        }

    if not valid_size(file_path):
        actual_size = os.path.getsize(file_path) / (1024 * 1024)
        return {
            'success': False,
            'message': f'File too large. Size: {actual_size:.2f}MB. Max: 5MB.'
        }

    file_hash = calculate_file(file_path)

    if is_duplicate(file_hash):
        return {
            'success': False,
            'message': f'Duplicate file. Already uploaded as {original_filename}.'
        }

    file_size = os.path.getsize(file_path)

    save_file_metadata(file_hash, original_filename, file_size)

    return {
        'success': True,
        'message': 'File uploaded successfully',
        'hash': file_hash,
        'filename': original_filename
    }

