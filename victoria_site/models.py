from datetime import date

from . import db, app

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


class User(db.Model):
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


with app.app_context():
    db.create_all()
