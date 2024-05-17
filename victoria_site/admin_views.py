from datetime import datetime
import os

from flask_admin.form.upload import FileUploadField  # , ImageUploadInput ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose   #, form
from wtforms.validators import DataRequired
from wtforms import MultipleFileField
from flask import request, url_for   #  redirect
from werkzeug.utils import secure_filename
from markupsafe import Markup

from . import app, db
from .models import Project, ProjectImage, Tag
# from .forms import ProjectForm
# from .utils import save_images

# with app.app_context():
#     tags = Tag.query.all()


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
        'image_path': MultipleFileField('Image')
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

    def on_model_change(self, form, model, is_created):
        files = request.files.getlist('image_path')
        if files:
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(os.path.join(app.static_folder, filepath))
                    image = ProjectImage(image_path=filepath, project=model)
                    db.session.add(image)
        return super(ProjectAdminView, self).on_model_change(form, model, is_created)

    def on_model_delete(self, model):
        for image in model.images:
            if image.image_path:
                try:
                    os.remove(os.path.join(app.static_folder, image.image_path))
                except Exception as e:
                    print(f"Error removing file: {e}")
        return super(ProjectAdminView, self).on_model_delete(model)

    # Надо подумать как это реализовать или не требуется
    # def delete_image(self, image):
    #     # Удаление изображения из файловой системы
    #     if image.image_path:
    #         try:
    #             os.remove(os.path.join(app.static_folder, image.image_path))
    #         except Exception as e:
    #             print(f"Error removing file: {e}")
    #     db.session.delete(image)
    #     db.session.commit()

    # @expose('/edit/', methods=('GET', 'POST'))
    # def edit_view(self):
    #     if request.method == 'POST' and 'remove_image' in request.form:
    #         image_id = request.form.get('remove_image')
    #         image = ProjectImage.query.get(image_id)
    #         self.delete_image(image)
    #     return super(ProjectAdminView, self).edit_view()


# class ProjectAdminView(ModelView):
#     form = ProjectForm

#     def create_form(self, obj=None):
#         form = super(ProjectAdminView, self).create_form(obj)
#         form.tags_select.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
#         return form

#     def on_model_change(self, form, model, is_created):
#         if is_created:
#             files = request.files.getlist('image_path')
#             for file in files:
#                 if file and file.filename:
#                     filename = secure_filename(file.filename)
#                     timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
#                     unique_filename = f"{timestamp}_{filename}"
#                     filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#                     file.save(os.path.join(app.static_folder, filepath))
#                     image = ProjectImage(image_path=filepath, project=model)
#                     db.session.add(image)
#             selected_tags = Tag.query.filter(Tag.id.in_(form.tags_select.data)).all()
#             model.tags = selected_tags  # Обновляем теги
#         super().on_model_change(form, model, is_created)
#         db.session.commit()  # Коммитим изменения

    # def create_view(self):
    #     if request.method == 'POST':
    #         form = self.create_form()
    #         if form.validate():
    #             model = self.model()
    #             self.on_model_change(form, model, is_created=True)
    #             db.session.add(model)
    #             db.session.commit()
    #             return redirect(self.get_url('.index_view'))
    #     return super(ProjectAdminView, self).create_view()

    # def create_form(self, obj=None):
    #     return super(ProjectAdminView, self).create_form(obj)

    # def edit_form(self, obj=None):
    #     return super(ProjectAdminView, self).edit_form(obj)


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
