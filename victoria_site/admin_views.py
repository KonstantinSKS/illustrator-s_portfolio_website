from datetime import datetime
import os

from flask_admin.form.upload import FileUploadField  # , ImageUploadInput ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose   # , form
from wtforms.validators import DataRequired
from wtforms import MultipleFileField, Field
from flask import request, url_for   # redirect
from werkzeug.utils import secure_filename
from markupsafe import Markup

from . import app, db
from .models import Project, ProjectImage  # , Tag
# from .forms import ProjectForm
# from .utils import save_images

# with app.app_context():
#     tags = Tag.query.all()


class ImageListWidget:
    def __call__(self, field, **kwargs):
        thumbnails = ''
        for image_path in field.data:
            thumbnails += Markup(
                f'<div>'
                f'<img src="{url_for("static", filename=image_path)}" width="100">'
                f'<input type="checkbox" name="delete_images" value="{image_path}"> Delete<br>'
                f'</div>'
            )
        return Markup(thumbnails)


class ImageListField(Field):
    widget = ImageListWidget()

    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.data = kwargs.get('images', [])

    def process_formdata(self, valuelist):
        self.data = valuelist


class AllProjectsView(AdminIndexView):
    @expose('/')
    def admin_projects(self):
        projects = Project.query.all()
        return self.render('admin/index.html', projects=projects)


class ProjectAdminView(ModelView):
    column_list = ['id', 'title', 'text', 'images', 'tags']
    column_sortable_list = ('id', 'title')  # Не работает по 'tags'
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'tags']
    form_excluded_columns = ['images']
    form_extra_fields = {
        'image_path': MultipleFileField('Image'),
        #'existing_images': ImageListField('Existing Images')
    }

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return ''

        return Markup(
            f'<img src="{url_for("static", filename=model.images[0].image_path)}" width="100">'
        )

    column_formatters = {
        'images': _list_thumbnail
    }

    def get_edit_form(self):
        form = super(ProjectAdminView, self).get_edit_form()
        form.existing_images = ImageListField('Existing Images')
        return form

    def edit_form(self, obj=None):
        form = super(ProjectAdminView, self).edit_form(obj)
        if obj and obj.images:
            image_paths = [image.image_path for image in obj.images]
            form.existing_images.data = image_paths
        else:
            form.existing_images.data = []
        return form

    def on_model_change(self, form, model, is_created):
        files = request.files.getlist('image_path')
        if files:
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                            unique_filename)
                    file.save(os.path.join(app.static_folder, filepath))
                    image = ProjectImage(image_path=filepath, project=model)
                    db.session.add(image)

        delete_image_paths = request.form.getlist('delete_images')
        if delete_image_paths:
            for image_path in delete_image_paths:
                image = ProjectImage.query.filter_by(
                    image_path=image_path).first()
                if image:
                    try:
                        os.remove(os.path.join(app.static_folder,
                                               image.image_path))
                    except Exception as e:
                        print(f"Error removing file: {e}")
                    db.session.delete(image)

        return super(ProjectAdminView, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        for image in model.images:
            if image.image_path:
                try:
                    os.remove(os.path.join(
                        app.static_folder, image.image_path))
                except Exception as e:
                    print(f"Error removing file: {e}")
        return super(ProjectAdminView, self).on_model_delete(model)


class TagsAdminView(ModelView):
    column_list = ['id', 'name']
    column_sortable_list = ('id', 'name')
    form_args = {  # Узнать где лучше, в модели или здесь???
        'name': dict(label='Name', validators=[DataRequired()]),
    }
    column_searchable_list = ['name']
    # column_exclude_list = ['project'] перенести в другую модель и доработать!


class ProjectImagesAdminView(ModelView):
    # can_create = False
    # can_delete = False
    # can_edit = False
    # form_extra_fields = {
    #     'image_path': ImageUploadField(
    #         'Images',
    #         base_path=os.path.join(app.static_folder, app.config['UPLOAD_FOLDER']),
    #         url_relative_path=os.path.join(app.static_folder, app.config['UPLOAD_FOLDER']),
    #         relative_path=os.path.join(app.static_folder, app.config['UPLOAD_FOLDER'])
    #     )
    # }
    ...


class BlogAdminView(ModelView):
    form_extra_fields = {
        'images': FileUploadField(
            'Images',
            base_path=app.static_folder,
            relative_path=os.path.join(app.config['UPLOAD_FOLDER']))
    }
    column_list = ['id', 'title', 'text', 'pub_date']  # 'images',
    column_sortable_list = ('id', 'title', 'pub_date')
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'pub_date']
    # form_args = { пригодится для других моделей
    #     'images': dict(label='Images', validators=[DataRequired()]),
    # }


class BlogImagesAdminView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
