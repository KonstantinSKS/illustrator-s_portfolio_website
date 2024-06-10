import os
from datetime import date

# from flask_security import (Security, RoleMixin, UserMixin,
#                             SQLAlchemyUserDatastore)
from flask_login import UserMixin

from . import db, app, manager

"""Table for project tags"""
project_tags = db.Table(
    'project_tags',
    db.Column('tag_id',
              db.Integer, db.ForeignKey('tag.id'),
              primary_key=True),
    db.Column('project_id',
              db.Integer, db.ForeignKey('project.id'),
              primary_key=True)
)


class Tag(db.Model):
    """Tags model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'#{self.name}'


class Project(db.Model):
    """Project model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    images = db.relationship('ProjectImage', back_populates='project',
                             lazy='subquery', cascade='all, delete-orphan',
                             order_by='ProjectImage.order')
    text = db.Column(db.Text, unique=False, nullable=True)
    tags = db.relationship('Tag', secondary='project_tags',
                           lazy='subquery',
                           backref=db.backref('projects', lazy=True))
    order = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f'Project: {self.title}'


class Blog(db.Model):
    """Blog model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    images = db.relationship('BlogImage', backref='blog', lazy=True,
                             cascade='all, delete-orphan',
                             order_by='BlogImage.order')
    text = db.Column(db.Text, unique=False, nullable=True)
    pub_date = db.Column(db.Date, unique=False, default=date.today)

    def __repr__(self):
        return f'<Blog {self.title}>'


class ProjectImage(db.Model):
    """Image model for projects"""
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(256), nullable=False)
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id'),
                           nullable=False)
    project = db.relationship('Project', back_populates='images')
    order = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f'<Image {self.image_path}>'


class BlogImage(db.Model):
    """Image model for blogs"""
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(256), nullable=False)
    blog_id = db.Column(db.Integer,
                        db.ForeignKey('blog.id'),
                        nullable=False)
    order = db.Column(db.Integer, nullable=True, default=0)

    def __repr__(self):
        return f'<Image {self.image_path}>'


@manager.user_loader
def load_user(user_id):
    # return db.session.query(User).get(user_id)
    # return User.query(user_id)
    return User.query.get(user_id)
    # return User.query.first()


class User(db.Model, UserMixin):
    """Admin model"""
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    artist_name = db.Column(db.String(120), nullable=True)
    image = db.Column(db.String(256), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text(512), nullable=True)
    instagram_link = db.Column(db.String(256), nullable=True)
    behance_link = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return self.username


# def create_default_user():
#     from .models import User
#     if not User.query.filter_by(email=os.getenv('EMAIL')).first():
#         user = User(
#             username=os.getenv('USERNAME'),
#             email=os.getenv('EMAIL'),
#             password=os.getenv('PASSWORD')
#         )
#         db.session.add(user)
#         db.session.commit()


# """Table for users roles"""
# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)
#     )


# class Role(db.Model, RoleMixin):
#     """Role model for User model"""
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))


# class User(db.Model, UserMixin):
#     """Admin model"""
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     artist_name = db.Column(db.String(120), nullable=True)
#     image = db.Column(db.String(256), nullable=True)
#     label = db.Column(db.String(256), nullable=True)
#     description = db.Column(db.Text(512), nullable=True)
#     instagram_link = db.Column(db.String(256), nullable=True)
#     behance_link = db.Column(db.String(256), nullable=True)
#     roles = db.relationship('Role', secondary='roles_users',
#                             backref=db.backref('users', lazy='dynamic'))

#     def __repr__(self):
#         return self.username


# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)


# @app.before_request
# def create_user():
#     if not user_datastore.find_user(email=os.getenv('EMAIL')):
#         user_datastore.create_user(
#             username=os.getenv('USERNAME'),
#             email=os.getenv('EMAIL'),
#             password=os.getenv('PASSWORD')
#         )
#     db.session.commit()


with app.app_context():
    db.create_all()
    # create_default_user()
    existing_user = User.query.filter_by(email=os.getenv('EMAIL')).first()

    if not existing_user:
        new_user = User(
            role='admin',
            username=os.getenv('USERNAME'),
            email=os.getenv('EMAIL'),
            password=os.getenv('PASSWORD')
        )
        db.session.add(new_user)
        db.session.commit()

    # if not user_datastore.find_user(email=os.getenv('EMAIL')):
    #     user_datastore.create_user(
    #         username=os.getenv('USERNAME'),
    #         email=os.getenv('EMAIL'),
    #         password=os.getenv('PASSWORD')
    #     )
    # db.session.commit()
