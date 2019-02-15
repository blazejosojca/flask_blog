import os
import secrets
from flask import current_app


def save_image_file(image_file):
    random_hex = secrets.token_hex(8)
    image_name, image_ext = os.path.split(image_file.filename)
    image_filename = '{0}{1}'.format(random_hex, image_ext)
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_filename)
    image_file.save(image_path)
    return image_filename
