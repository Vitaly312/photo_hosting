from flask_wtf import FlaskForm
from wtforms import (IntegerField, TextAreaField,
                     SubmitField, MultipleFileField)
from wtforms.validators import DataRequired, NumberRange



class PhotoUploadForm(FlaskForm):
    class Meta:
        locales = ['ru_RU', 'ru']

        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)
    photo = MultipleFileField(validators=[DataRequired()])
    description = TextAreaField("Введите описание фотографии(не более 1000 символов, \
заполнять это поле необязательно):")
    storage_time = IntegerField("Введите срок хранения изображения(кол-во дней, не более 90):", validators=[NumberRange(1, 90)])
    submit = SubmitField("Загрузить")