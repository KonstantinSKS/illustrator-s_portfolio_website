# from datetime import datetime
import os

from flask_admin.form.upload import FileUploadField
from flask_admin.contrib.sqla import ModelView

from . import app


class ProjectAdminView(ModelView):
    form_extra_fields = {
        'images': FileUploadField(
            'Images',
            base_path=app.static_folder,
            relative_path=os.path.join(app.config['UPLOAD_FOLDER']))
    }
