from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from . import app, db
from .models import Project, Tag, Blog, ProjectImage, BlogImage


admin = Admin(app, name='My_art', template_mode='bootstrap4')
admin.add_view(ModelView(Project, db.session, name='Projects'))
admin.add_view(ModelView(Tag, db.session, name='Tags'))
admin.add_view(ModelView(ProjectImage, db.session, name='Project_images'))
admin.add_view(ModelView(Blog, db.session, name='Blogs'))
admin.add_view(ModelView(BlogImage, db.session, name='Blog_images'))
