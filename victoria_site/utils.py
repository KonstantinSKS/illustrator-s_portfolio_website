from datetime import datetime
import os

from flask import request  # flash
from werkzeug.utils import secure_filename
# from wtforms import MultipleFileField

from . import app
from .models import ProjectImage

# import os

# from flask import url_for
# from markupsafe import Markup

# from . import app


# def _list_thumbnail(view, context, model, name):
#     if not model.images:
#         return ''
#     url = url_for('static', filename=os.path.join(app.config['UPLOAD_FOLDER'],
#                                                   model.images))
#     if model.images.split('.')[-1] in app.config['ALLOWED_EXTENSIONS']:
#         return Markup(f'<img src={url}" width="100">')


def save_images():
    project = request.get_data('project.id')
    files = request.files.getlist('image_path')
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                    unique_filename)
            file.save(os.path.join(app.static_folder, filepath))
            image = ProjectImage(image_path=filepath, project=project)
            return image
