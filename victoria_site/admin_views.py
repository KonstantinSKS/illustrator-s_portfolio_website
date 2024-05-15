# from datetime import datetime
import os

from flask_admin.form.upload import ImageUploadField, FileUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from wtforms.validators import DataRequired
# from flask import url_for
# from markupsafe import Markup

from . import app
from .models import Project
# from .utils import save_images


class AllProjectsView(AdminIndexView):
    @expose('/')
    def admin_projects(self):
        projects = Project.query.all()
        return self.render('admin/index.html', projects=projects)


class ProjectAdminView(ModelView):
    form_extra_fields = {
        'images': ImageUploadField(
            'Images',
            base_path=os.path.join(app.static_folder, app.config['UPLOAD_FOLDER']),
            url_relative_path=app.config['UPLOAD_FOLDER'],
            # validators=[DataRequired()],
            # thumbnail_size=(100, 100, True),
            # multiple_files=True
        )
    }
    column_list = ['id', 'title', 'text', 'images', 'tags']
    column_sortable_list = ('id', 'title')  # Не работает по 'tags'
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'tags']

    def create_form(self, obj=None):
        return super(ProjectAdminView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(ProjectAdminView, self).edit_form(obj)


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
