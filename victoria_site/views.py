# from datetime import datetime
# import os

from flask import render_template, request  # , redirect, flash, url_for
# from werkzeug.utils import secure_filename

from . import app  # , db
from .models import Project, Tag, Blog
# from .forms import BLogForm

DESCRIPTION = (
    'My name is Victoria Stebleva,\n'
    'I am an international published illustrator and author-illustrator currently living in Serbia.\n'
    'My portfolio includes non-fiction, middle-grade, activity books, graphic novel, wimmelbuch,\n'
    'editorial illustrations and even more.\n'
    'I am fond of motorbike traveling, nonfiction literature, rock music, and pets.\n'
    'Select clients include: Scholastic, Penguin Random House, Magic Cat, Usborne, Highlights,\n'
    'Yoyo Books, Wonderbly.'
)

USER_INFO = {
        "name": "VICTORIA STEBLEVA",
        "description": DESCRIPTION,  # Вынести в админку
        "image": "/static/img/avatar885138196.jpg",
        "email": "vikastebleva@gmail.com",
        "instagram": "https://www.instagram.com/vika_stebleva/",
        "behance": "https://www.behance.net/vika_stebleva"
    }

# DESCRIPTION = """
#     My name is Victoria Stebleva,
#     I am an international published illustrator and author-illustrator currently living in Serbia.
#     My portfolio includes non-fiction, middle-grade, activity books, graphic novel, wimmelbuch,
#     editorial illustrations and even more.
#     I am fond of motorbike traveling, nonfiction literature, rock music, and pets.
#     Select clients include: Scholastic, Penguin Random House, Magic Cat, Usborne, Highlights,
#     Yoyo Books, Wonderbly.
# """


@app.route('/')
def index_view():
    """Renders main page with projects"""
    tag_filter = request.args.get('tag')
    if tag_filter and tag_filter != 'all':
        projects = Project.query.join(Project.tags).filter(
            Tag.name == tag_filter).all()
    else:
        projects = Project.query.order_by(Project.order).all()
        # projects = Project.query.all()
    tags = Tag.query.all()
    return render_template('main.html',
                           projects=projects,
                           tags=tags,
                           current_tag=tag_filter,
                           user=USER_INFO)


@app.route('/projects/<int:id>')
def project_view(id):
    """Renders project page"""
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project,
                           user=USER_INFO)


@app.route('/about')
def about_view():
    """Renders information about an artist"""
    # user_info = {
    #     "name": "Victoria Stebleva",
    #     "description": DESCRIPTION,  # Вынести в админку
    #     "image_path": "/static/img/avatar885138196.jpg",
    #     "email": "vikastebleva@gmail.com",
    #     "instagram": "https://www.instagram.com/vika_stebleva/",
    #     "behance": "https://www.behance.net/vika_stebleva"
    # }
    return render_template('about.html', user=USER_INFO)


# ДОРАБОТАТЬ БЛОГИ!!!!! название вью, шаблоны!!!


@app.route('/blogs')
def all_blogs_view():
    """Renders main page with blogs"""
    blogs = Blog.query.all()
    return render_template('all_blogs.html', blogs=blogs,
                           user=USER_INFO)


@app.route('/blogs/<int:id>')
def blog_view(id):
    """Renders blog page"""
    blog = Blog.query.get_or_404(id)
    return render_template('blog.html', blog=blog,
                           user=USER_INFO)


# @app.route('/copy-email')
# def copy_email():
#     flash('The email address has been copied.')
#     return redirect(url_for('about_view'))

# @app.route('/add_blog', methods=['GET', 'POST'])
# def add_blog():
#     form = BLogForm()
#     if form.validate_on_submit():
#         blog = Blog(
#             title=form.title.data,
#             text=form.text.data
#         )
#         db.session.add(blog)
#         filename = None
#         files = request.files.getlist('image')
#         if files:
#             for file in files:
#                 if file and file.filename:
#                     filename = secure_filename(file.filename)
#                     timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
#                     unique_filename = f"{timestamp}_{filename}"
#                     filepath = os.path.join(app.config['UPLOAD_FOLDER'],
#                                             unique_filename)
#                     file.save(os.path.join(app.static_folder, filepath))
#                     image = BlogImage(image_path=filepath, blog=blog)
#                     db.session.add(image)
#         db.session.commit()
#         return redirect(url_for('all_blogs_view'))
#     return render_template('add_blog.html', form=form)


# @app.route('/add_project', methods=['GET', 'POST'])
# def add_project():
#     form = ProjectForm()
#     form.tags_select.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
#     if form.validate_on_submit():
#         project = Project(
#             title=form.title.data,
#             text=form.text.data
#         )
#         db.session.add(project)
#         files = request.files.getlist('image_path')
#         for file in files:
#             if file and file.filename:
#                 filename = secure_filename(file.filename)
#                 timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
#                 unique_filename = f"{timestamp}_{filename}"
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'],
#                                         unique_filename)
#                 file.save(os.path.join(app.static_folder, filepath))
#                 image = ProjectImage(image_path=filepath, project=project)
#                 db.session.add(image)
#         selected_tags = Tag.query.filter(
#             Tag.id.in_(form.tags_select.data)).all()
#         project.tags.extend(selected_tags)
#         db.session.commit()
#         return redirect(url_for('index_view'))
#     return render_template('add_project.html', form=form)
