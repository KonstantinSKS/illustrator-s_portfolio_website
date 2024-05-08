from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SubmitField, FileField,
                     TextAreaField, SelectMultipleField
                     )  # MultipleFileField widgets
from wtforms.validators import Length, Optional, DataRequired
# SelectMultipleField SelectField ??
from .models import Tag
from . import app

with app.app_context():
    tags = Tag.query.all()


# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()


class ProjectForm(FlaskForm):
    title = StringField(
        'Введите заголовок проекта',
        validators=[Length(1, 128), Optional()]
    )
    image_path = FileField('Загрузить изображение/видео', validators=[
        FileRequired(),
        FileAllowed(app.config['ALLOWED_EXTENSIONS'],
                    'Недопустимый формат файла!')
    ])
    # image_path = MultipleFileField(
    #     'Загрузите свои изображения',
    #     validators=[DataRequired(message='Обязательное поле')]
    # )
    text = TextAreaField(
        'Описание проекта',
        validators=[Length(1, 256), Optional()]  # уточнить max длину текста
    )
    tags_select = SelectMultipleField(
        'Выберите тэги',
        validators=[DataRequired()],
        choices=[tag.name for tag in tags])
    # tags_select = SelectMultipleField('Выберите тэги', coerce=int)

    submit = SubmitField('Добавить')


class BLogForm(FlaskForm):
    title = StringField(
        'Введите заголовок записи',
        validators=[Length(1, 128), Optional()]
    )
    image = FileField('Загрузить изображение/видео', validators=[
        FileAllowed(app.config['ALLOWED_EXTENSIONS'],
                    'Недопустимый формат файла!')
    ])
    text = TextAreaField(
        'Ваша запись в блоге',
        validators=[Length(1, 256), Optional()]  # уточнить max длину текста
    )
    submit = SubmitField('Добавить')
