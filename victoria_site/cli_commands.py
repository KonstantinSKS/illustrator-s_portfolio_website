import os
from dotenv import load_dotenv

import click

from . import app, db
from .models import User

load_dotenv()


@app.cli.command('load_admin_profile')
def load_admin_profile_command():
    """Creates Admin instance if not exists."""
    existing_user = User.query.filter_by(email=os.getenv('EMAIL')).first()
    if not existing_user:
        new_user = User(
            role=os.getenv('ROLE'),
            username=os.getenv('USERNAME'),
            email=os.getenv('EMAIL'),
            password=os.getenv('PASSWORD')
        )
        db.session.add(new_user)
        db.session.commit()
    click.echo('Admin profile was loaded.')
