from datetime import date

from . import db

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'#{self.name}'


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    images = db.relationship('ProjectImage', backref='project', lazy=True,
                             cascade='all, delete-orphan')
    text = db.Column(db.Text, unique=True, nullable=True)
    tags = db.relationship(
        'Tag', secondary=project_tags, lazy='subquery',
        backref=db.backref('projects', lazy=True,
                           cascade='all, delete-orphan', single_parent=True))

    def __repr__(self):
        return f'Project: {self.title}'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    images = db.relationship('BlogImage', backref='blog', lazy=True,
                             cascade='all, delete-orphan')
    text = db.Column(db.Text, unique=True, nullable=True)
    pub_date = db.Column(db.Date, unique=False, default=date.today)

    def __repr__(self):
        return f'<Blog {self.title}>'


class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(256), nullable=False)
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id'),
                           nullable=False)

    def __repr__(self):
        return f'<Image {self.image_path}>'


class BlogImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(256))  # , nullable=False ? True
    blog_id = db.Column(db.Integer,
                        db.ForeignKey('blog.id'),
                        nullable=False)

    def __repr__(self):
        return f'<Image {self.image_path}>'
