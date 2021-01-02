from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class keywordRequestForm(FlaskForm):
    keyword = StringField('Keyword(s):', validators=[DataRequired(), Length(min=2)])

    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    """


    submit = SubmitField('Submit')

