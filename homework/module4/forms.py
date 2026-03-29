from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from validators import number_length, NumberLength

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(message='Email обязателен'),
        Email(message='Некорректный формат email')
    ])
    phone = IntegerField('Phone', validators=[
        InputRequired(message='Телефон обязателен'),
        number_length(min_len=10, max_len=10, message='Номер телефона должен состоять из 10 цифр')
    ])
    name = StringField('Name', validators=[
        InputRequired(message='Имя обязательно'),
        Length(max=100)
    ])
    address = StringField('Address', validators=[
        InputRequired(message='Адрес обязателен')
    ])
    index = IntegerField('Index', validators=[
        InputRequired(message='Индекс обязателен'),
        number_length(min_len=5, max_len=6, message='Индекс должен содержать 5 или 6 цифр')
    ])
    comment = TextAreaField('Comment', validators=[])
