from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField, SelectField
from wtforms.validators import Length,EqualTo,Email,DataRequired , ValidationError

from flask import flash
class Inputform(FlaskForm):

    
    source = StringField(
        'Source Location',
        validators=[DataRequired()],
        render_kw={
            "list": "source-cities",  # Datalist ID
            "placeholder": "Select or type any city",
            "class": "form-control city-search",
            "autocomplete": "off"
        }
    )
    
    destination = StringField(
        'Destination Location',
        validators=[DataRequired()],
        render_kw={
            "list": "dest-cities",
            "placeholder": "Select or type any city",
            "class": "form-control city-search", 
            "autocomplete": "off"
        }
    )
    
    preference = SelectField(
        'Route Preference',
        choices=[('','--Select Preference--'),('distance','Shortest Distance'),('toll','Minimum Toll'),('time','Shortest Time ( Recommended )')], validators=[DataRequired()])
       
    
    submit = SubmitField('Find the Route')
    
class RegisterForm(FlaskForm):
    
   username= StringField(label='Username', validators=[Length(min=2, max=30),DataRequired()])
   email_address= StringField(label='Email',validators=[Email(),DataRequired()])
   password1 = PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
   password2 = PasswordField(label = 'Confirm Password',validators=[DataRequired(), EqualTo('password1', message='Passwords must match')])
   
   def validate_password2(self, field):
       if self.password1.data != field.data:
           raise ValidationError('Passwords must match')
   submit = SubmitField(label = 'Create Account')

class LoginForm(FlaskForm):
    username= StringField(label='Username', validators=[DataRequired()])
    password= PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label = 'Sign in')

    


    
