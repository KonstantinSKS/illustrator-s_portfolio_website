# from datetime import datetime
# import os

from flask import render_template, request  # , redirect, flash, url_for
# from flask_login import login_user, logout_user, login_required
# from werkzeug.security import check_password_hash
# from werkzeug.utils import secure_filename

from . import app  # , db
from .models import Project, Tag, Blog, User
# from .forms import BLogForm


DESCRIPTION = """
    My name is Victoria Stebleva,
    I am an international published illustrator and author-illustrator currently living in Serbia.
    My portfolio includes non-fiction, middle-grade, activity books, graphic novel, wimmelbuch,
    editorial illustrations and even more.
    I am fond of motorbike traveling, nonfiction literature, rock music, and pets.
    Select clients include: Scholastic, Penguin Random House, Magic Cat, Usborne, Highlights,
    Yoyo Books, Wonderbly.
"""


USER_INFO = {
        "name": "VICTORIA STEBLEVA",
        "description": DESCRIPTION,  # Вынести в админку
        "image": "/static/img/avatar885138196.jpg",
        "email": "vikastebleva@gmail.com",
        "instagram": "https://www.instagram.com/vika_stebleva/",
        "behance": "https://www.behance.net/vika_stebleva"
    }


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login = request.form.get('login')
#     password = request.form.get('password')
#     if login and password:
#         user = User.query.filter_by(username=login).first()
#         if user and user.password == password:
#             login_user(user)
#             next_page = request.args.get('next')
#             # return redirect(next_page)
#             return redirect(next_page or url_for('admin.index'))
#         else:
#             flash('Login or password is not correct.')
#     else:
#         flash('Please fill login and password fields.')
#     return render_template('admin/login.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     pass


# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('admin.index'))


# @app.after_request
# def redirect_to_signin(response):
#     if response.status_code == 401:
#         return redirect(url_for('login') + '?next=' + request.url)
#     return response


@app.route('/')
def index_view():
    """Renders main page with projects"""
    tag_filter = request.args.get('tag')
    if tag_filter and tag_filter != 'all':
        projects = Project.query.join(Project.tags).filter(
            Tag.name == tag_filter).all()
    else:
        projects = Project.query.order_by(Project.order).all()
    tags = Tag.query.all()
    return render_template('main.html',
                           projects=projects,
                           tags=tags,
                           current_tag=tag_filter,
                           user=User.query.first())


@app.route('/projects/<int:id>')
def project_view(id):
    """Renders project page"""
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project,
                           user=User.query.first())


@app.route('/about')
def about_view():
    """Renders information about an artist"""
    return render_template('about.html', user=User.query.first())


# ДОРАБОТАТЬ БЛОГИ!!!!! название вью, шаблоны!!!


@app.route('/blogs')
def all_blogs_view():
    """Renders main page with blogs"""
    blogs = Blog.query.all()
    return render_template('all_blogs.html', blogs=blogs,
                           user=User.query.first())


@app.route('/blogs/<int:id>')
def blog_view(id):
    """Renders blog page"""
    blog = Blog.query.get_or_404(id)
    return render_template('blog.html', blog=blog,
                           user=User.query.first())


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
