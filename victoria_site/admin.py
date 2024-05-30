from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

from . import app, db
from .models import Project, Tag, Blog, ProjectImage, BlogImage
from .admin_views import (ProjectAdminView, AllProjectsView, TagsAdminView,
                          BlogAdminView, ProjectImagesAdminView)  # ProjectImagesAdminView BlogImagesAdminView


admin = Admin(app, 'My_art', index_view=AllProjectsView(),
              template_mode='bootstrap4', url='/')
# admin.add_view(ModelView(Project, db.session, name='Projects'))
admin.add_view(ProjectAdminView(Project, db.session, name='Projects'))
admin.add_view(TagsAdminView(Tag, db.session, name='Tags'))
admin.add_view(ProjectImagesAdminView(ProjectImage, db.session,
                                      name='Project_images'))
admin.add_view(BlogAdminView(Blog, db.session, name='Blogs'))
# admin.add_view(BlogImagesAdminView(BlogImage, db.session, name='Blog_images'))
