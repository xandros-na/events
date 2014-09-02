from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, RadioField
from wtforms.validators import Required, Length

class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 12)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class EventForm(Form):
    title = StringField('Title', validators=[Required(), Length(1, 128)])
    room = StringField('Room', validators=[Required(), Length(1, 12)])
    date = DateTimeField('Date', description='hint: 2014-07-12 16:30:00 converts to Jul 12 2014, 4:30:00 PM')
    submit = SubmitField('Post')

    def from_model(self, event):
        self.title = event.title
        self.room = event.room
        self.date = event.thedate

    def to_model(self, event, posted_date):
        event.title = self.title.data
        event.room = self.room.data
        event.thedate = self.date.data
        event.posted_date = posted_date

class UserForm(Form):
    first_name = StringField('First Name', validators=[Required(), Length(1,16)])
    last_name = StringField('Last Name', validators=[Required(), Length(1,16)])
    student_num = StringField('Student Number', validators=[Required(), Length(9,9, 'Student number must be 9 characters long')])
    payment = RadioField('Payment', choices=[('1','$ 5.00 This session only'), ('2','$10.00 One year'), ('3','$20.00 Lifetime')])
    submit = SubmitField('Register')
