from flask import render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Renders page not found"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Renders internal server error page"""
    db.session.rollback()
    return render_template('500.html'), 500
