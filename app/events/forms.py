from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import Required, Length

class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class EventForm(Form):
    title = StringField('Title', validators=[Required(), Length(1, 128)])
    room = StringField('Room', validators=[Required(), Length(1, 12)])
    date = DateField('Date')
    submit = SubmitField('Post')

class UserForm(Form):
    first_name = StringField('First Name', validators=[Required(), Length(1,16)])
    last_name = StringField('Last Name', validators=[Required(), Length(1,16)])
    student_num = IntegerField('Student Number', validators=[Required(), Length(1,9)])
    submit = SubmitField('Register')
