
from flask import request, url_for, redirect, flash  # render_template,
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.form import ImageUploadField
from flask_login import login_user, login_required, logout_user, current_user
# from flask_security import login_required
from markupsafe import Markup
from wtforms.validators import DataRequired, NumberRange, Email
from wtforms import MultipleFileField

from . import app
from .models import Project, ProjectImage, Blog, BlogImage, User
from .utils import (ImageListField, save_images, delete_images_in_editing,
                    delete_images, order_images, generate_image_name)

AVAILABLE_USER_TYPES = [
    (u'admin', u'admin'),
    (u'author', u'author'),
    (u'editor', u'editor')
]

# ИМПОРТИРОВАТЬ ТОЛЬКО FLASK LOGIN, FLASK SEQURITY УБРАТЬ!!!


class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


# class AuthAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login'))


class AuthBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


class LoginView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                user = User.query.filter_by(username=username).first()
                if user and user.password == password:
                    login_user(user)
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('admin.index'))
                else:
                    flash('Login or password is not correct.')
            else:
                flash('Please fill login and password fields.')
        return self.render('admin/login.html')


class LogoutView(BaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('admin.index'), 302)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('admin.index'))
    return response


class AllProjectsView(AdminIndexView):
    """A custom admin view for displaying all projects."""
    @expose('/')
    # @login_required
    def admin_projects(self):
        projects = Project.query.order_by(Project.order).all()
        # projects = Project.query.all()
        return self.render('admin/index.html', projects=projects)


class AllBlogsView(AuthBaseView):
    """A custom admin view for displaying all blogs."""
    @expose('/')
    def admin_blogs(self):
        blogs = Blog.query.all()
        return self.render('admin/blogs_preview.html', blogs=blogs)


class UserAdminView(AuthModelView):
    """A custom admin view for User model."""
    # column_list = ['role', 'username', 'email', 'password', 'artist_name', 'image', 'label', 'description', 'instagram_link', 'behance_link']
    column_labels = {
        'image': 'Avatar',
        'description': 'About me'
    }
    can_delete = True  # НАДО ЛИ ??
    form_args = {
        'role': dict(validators=[DataRequired()]),
        'username': dict(validators=[DataRequired()]),
        'email': dict(validators=[Email()]),
        'password': dict(validators=[DataRequired()]),
    }
    form_choices = {
        'role': AVAILABLE_USER_TYPES
    }

    def _image_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup(
            f'<img src="{url_for("static", filename=model.image)}" width="100">'
        )

    def _label_thumbnail(view, context, model, name):
        if not model.label:
            return ''

        return Markup(
            f'<img src="{url_for("static", filename=model.label)}" width="100">'
        )

    column_formatters = {
        'image': _image_thumbnail,
        'label': _label_thumbnail
    }
    form_extra_fields = {
        'image': ImageUploadField(
            'Image',
            base_path=app.static_folder,
            relative_path=app.config['USER_IMAGES'],
            namegen=generate_image_name
        ),
        'label': ImageUploadField(
            'Label',
            base_path=app.static_folder,
            relative_path=app.config['USER_IMAGES'],
            namegen=generate_image_name
        )
    }
    column_descriptions = {
        'artist_name': ('Enter your first and last name '
                        'to display them on the site.'),
        'image': ('Upload your avatar '
                  'to display it on the about + contact page.'),
        'label': ('Upload an image if you want to display it '
                  'instead of your name on the site.'),  # ВОзможно надо указать размеры изображения!!!
        'description': 'Tell us about yourself here.'
    }
    column_exclude_list = ['password']
    column_editable_list = ['role']


class ProjectAdminView(AuthModelView):
    """A custom admin view for creating and editing all projects."""
    column_list = ['id', 'order', 'title', 'text', 'images', 'tags']
    column_sortable_list = ['id', 'order', 'title']
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'tags']
    column_editable_list = ['order']
    form_excluded_columns = ['images']
    form_extra_fields = {
        'image_path': MultipleFileField('Image'),
    }
    form_args = {
        'order': {
            'validators': [NumberRange
                           (min=0, message="Order must be a positive number")]
        }
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

        order_images(model)

        return super(ProjectAdminView, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        delete_images(model)

        return super(ProjectAdminView, self).on_model_delete(model)


class TagsAdminView(AuthModelView):
    """A custom admin view for creating and editing all tags."""
    column_list = ['id', 'name']
    column_sortable_list = ('id', 'name')
    form_args = {
        'name': dict(label='Name', validators=[DataRequired()]),
    }
    column_searchable_list = ['name']
    form_excluded_columns = ['projects']


class ProjectImagesAdminView(AuthModelView):
    """A custom admin view for displaying images of all projects."""
    column_list = ['id', 'project.title', 'project_id', 'images']
    column_sortable_list = ['id', 'project.title', 'project_id']
    column_searchable_list = ['project.title']

    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''
        return Markup(
            f'<img src="{url_for("static", filename=model.image_path)}" width="100">'
        )

    column_formatters = {
        'images': _list_thumbnail
    }

    can_create = False
    can_delete = False
    can_edit = False


class BlogAdminView(AuthModelView):
    """A custom admin view for creating and editing all blogs."""
    column_list = ['id', 'title', 'text', 'images', 'pub_date']
    column_sortable_list = ('id', 'title', 'pub_date')
    column_searchable_list = ['title', 'text']
    column_filters = ['title', 'pub_date']
    form_excluded_columns = ['images']
    form_extra_fields = {
        'image_path': MultipleFileField('Image'),
    }
    form_args = {
        'order': {
            'validators': [NumberRange
                           (min=0, message="Order must be a positive number")]
        }
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

        order_images(model)

        return super(BlogAdminView, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        delete_images(model)

        return super(BlogAdminView, self).on_model_delete(model)


class BlogImagesAdminView(AuthModelView):
    """A custom admin view for displaying images of all blogs."""
    column_list = ['id', 'blog.title', 'blog_id', 'images']
    column_sortable_list = ['id', 'blog.title', 'blog_id']
    column_searchable_list = ['blog.title']

    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''
        return Markup(
            f'<img src="{url_for("static", filename=model.image_path)}" width="100">'
        )

    column_formatters = {
        'images': _list_thumbnail
    }

    can_create = False
    can_delete = False
    can_edit = False
