from flask import render_template, request

from . import app, cache
from .models import Project, Tag, Blog, User
from .utils import make_cache_key


@app.route('/')
@cache.cached(timeout=60, key_prefix=make_cache_key)
def index_view():
    """Renders main page with projects."""
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
@cache.cached(timeout=60)
def project_view(id):
    """Renders project page."""
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project,
                           user=User.query.first())


@app.route('/about')
@cache.cached(timeout=60)
def about_view():
    """Renders information about an artist."""
    return render_template('about.html', user=User.query.first())


@app.route('/blogs')
@cache.cached(timeout=60)
def all_blogs_view():
    """Renders main page with blogs."""
    blogs = Blog.query.all()
    return render_template('all_blogs.html', blogs=blogs,
                           user=User.query.first())


@app.route('/blogs/<int:id>')
@cache.cached(timeout=60)
def blog_view(id):
    """Renders blog page."""
    blog = Blog.query.get_or_404(id)
    return render_template('blog.html', blog=blog,
                           user=User.query.first())
