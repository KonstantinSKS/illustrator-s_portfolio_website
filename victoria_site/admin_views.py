# import os

from flask import request, url_for   # redirect
# from flask_admin.form.upload import FileUploadField  # , ImageUploadInput ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose   # , form
from markupsafe import Markup
from wtforms.validators import DataRequired
from wtforms import MultipleFileField  # , Field

# from . import app  # , db
from .models import Project, ProjectImage, BlogImage  # , Tag
from .utils import (ImageListField, save_images, delete_images_in_editing,
                    delete_images)


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
            save_images(files, ProjectImage, model, obj_attr='project')

        delete_image_paths = request.form.getlist('delete_images')
        if delete_image_paths:
            delete_images_in_editing(delete_image_paths, ProjectImage)

        return super(ProjectAdminView, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        delete_images(model)

        return super(ProjectAdminView, self).on_model_delete(model)


class TagsAdminView(ModelView):
    column_list = ['id', 'name']
    column_sortable_list = ('id', 'name')
    form_args = {  # Узнать где лучше, в модели или здесь???
        'name': dict(label='Name', validators=[DataRequired()]),
    }
    column_searchable_list = ['name']
    form_excluded_columns = ['projects']
    # column_exclude_list = ['project'] перенести в другую модель и доработать!


# class ProjectImagesAdminView(ModelView):
#     can_create = False
#     can_delete = False
#     can_edit = False


class BlogAdminView(ModelView):
    column_list = ['id', 'title', 'text', 'images', 'pub_date']  # 'images',
    column_sortable_list = ('id', 'title', 'pub_date')
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'pub_date']
    form_excluded_columns = ['images']
    form_extra_fields = {
        'image_path': MultipleFileField('Image'),
    }
    # form_args = { пригодится для других моделей
    #     'images': dict(label='Images', validators=[DataRequired()]),
    # }

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
        form = super(BlogAdminView, self).get_edit_form()
        form.existing_images = ImageListField('Existing Images')
        return form

    def edit_form(self, obj=None):
        form = super(BlogAdminView, self).edit_form(obj)
        if obj and obj.images:
            image_paths = [image.image_path for image in obj.images]
            form.existing_images.data = image_paths
        else:
            form.existing_images.data = []
        return form

    def on_model_change(self, form, model, is_created):
        files = request.files.getlist('image_path')
        if files:
            save_images(files, BlogImage, model, obj_attr='blog')

        delete_image_paths = request.form.getlist('delete_images')
        if delete_image_paths:
            delete_images_in_editing(delete_image_paths, BlogImage)

        return super(BlogAdminView, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        delete_images(model)

        return super(BlogAdminView, self).on_model_delete(model)


# class BlogImagesAdminView(ModelView):
#     can_create = False
#     can_delete = False
#     can_edit = False
