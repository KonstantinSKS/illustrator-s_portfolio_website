from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView

from . import app, db
from .models import Project, Tag, Blog, ProjectImage, BlogImage, User
from .admin_views import (ProjectAdminView, AllProjectsView, TagsAdminView,
                          BlogAdminView, ProjectImagesAdminView,
                          BlogImagesAdminView, AllBlogsView, LoginView,
                          LogoutView, UserAdminView)


admin = Admin(app, 'Go to MyArt', index_view=AllProjectsView(),
              template_mode='bootstrap4', url='/')
admin.add_view(LoginView(name='Login', url='login'))
admin.add_view(UserAdminView(User, db.session, name='Your_profile'))
# admin.add_view(ModelView(User, db.session))
admin.add_view(ProjectAdminView(Project, db.session, name='Projects'))
admin.add_view(ProjectImagesAdminView(ProjectImage, db.session,
                                      name='Project_images'))
admin.add_view(TagsAdminView(Tag, db.session, name='Tags'))
admin.add_view(AllBlogsView(name='Blogs_preview', endpoint='blogs_preview'))
admin.add_view(BlogAdminView(Blog, db.session, name='Blogs'))
admin.add_view(BlogImagesAdminView(BlogImage, db.session, name='Blog_images'))
admin.add_view(LogoutView(name='Logout', endpoint='index'))
