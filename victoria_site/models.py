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
    name = db.Column(db.String(50), unique=True)
    name.verbose_name = 'Название тэга'

    def __repr__(self):
        return f'#{self.name}'


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    title.verbose_name = 'Заголовок проекта'
    images = db.relationship('ProjectImage', backref='project', lazy=True)
    images.verbose_name = 'Изображения'
    text = db.Column(db.Text, unique=True, nullable=True)
    text.verbose_name = 'Описание проекта'
    tags = db.relationship(
        'Tag', secondary=project_tags, lazy='subquery',
        backref=db.backref('projects', lazy=True))
    tags.verbose_name = 'Тэги'

    def __repr__(self):
        return f'Project: {self.title}'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    title.verbose_name = 'Заголовок блога'
    images = db.relationship('BlogImage', backref='blog', lazy=True)
    images.verbose_name = 'Изображения'
    text = db.Column(db.Text, unique=True, nullable=True)
    text.verbose_name = 'Текст блога'
    pub_date = db.Column(db.Date, unique=False, default=date.today)
    pub_date.verbose_name = 'Дата публикации'

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
