from datetime import datetime
import os

from flask import url_for
from markupsafe import Markup
from werkzeug.utils import secure_filename
from wtforms import Field

from . import app, db


class ImageListWidget:
    """ Creates HTML markup for displaying form fields with thumbnails. """
    def __call__(self, field, **kwargs):
        thumbnails = ''
        for i, image_path in enumerate(field.data):
            thumbnails += Markup(
                f'<div>'
                f'<img src="{url_for("static", filename=image_path)}" width="100">'
                f'<input type="checkbox" name="delete_images" value="{image_path}"> Delete<br>'
                f'<input type="number" name="order_{i}" value="{i}" min="0" step="1"> Order<br>'
                f'</div>'
            )
        return Markup(thumbnails)


class ImageListField(Field):
    """Custom form fields for thumbnails."""
    widget = ImageListWidget()

    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.data = kwargs.get('images', [])

    def process_formdata(self, valuelist):
        self.data = valuelist


def save_images(files, model, obj, obj_attr='project'):
    """Saves images to the static/media folder
                    and
    generates unique file names when saving."""
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                    unique_filename)
            file.save(os.path.join(app.static_folder, filepath))
            image = model(image_path=filepath)
            setattr(image, obj_attr, obj)  # ВЫЯСНИТЬ как работает эта функция!
            db.session.add(image)


def delete_images_in_editing(delete_image_paths, model):
    """Allows you to delete images in edit mode"""
    for image_path in delete_image_paths:
        image = model.query.filter_by(
            image_path=image_path).first()
        if image:
            try:
                os.remove(os.path.join(app.static_folder,
                                       image.image_path))
            except Exception as e:
                print(f"Error removing file: {e}")
            db.session.delete(image)


def delete_images(model):
    """Deletes images when the model object is deleted."""
    for image in model.images:
        if image.image_path:
            try:
                os.remove(os.path.join(
                    app.static_folder, image.image_path))
            except Exception as e:
                print(f"Error removing file: {e}")
