from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import *
from wtforms.validators import *
from webapp.covid19 import *
import datetime as dt

from webapp.plots_module import Plot as pt





class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')






keys=list(Confirmed.dict.keys());
country_choices=[]
for key in keys:
	sub=(key,key)
	country_choices.append(sub)

scale_choices=[("linear","Linear"), ("log", "Logarithmic")]
x_data_choices=pt.data_keys.copy()
y_data_choices=pt.data_keys.copy()
y_data_choices.pop(0)




first_date=Confirmed.str_to_obj(Confirmed.fields[5])
last_date=Confirmed.str_to_obj(Confirmed.latest_date())





class GraphForm(FlaskForm):
	countries = SelectMultipleField('Select Countries', choices=country_choices, validators=[DataRequired(message='Please select one or more choices.')])
	start_date = DateField('Start Date(dd-mm-yy)', format='%d-%m-%y', default=first_date, validators=[DataRequired()])#validators
	end_date = DateField('End Date(dd-mm-yy)', format='%d-%m-%y', default=last_date, validators=[DataRequired()])
	x_field	= SelectField('X Axis Data', choices=x_data_choices, default='days')
	y_field = SelectField('Y Axis Data', choices=y_data_choices)
	x_scale = SelectField('X Axis Scale', choices=scale_choices, default='linear')
	y_scale = SelectField('Y Axis Scale', choices=scale_choices, default='linear')
	line_width = FloatField('Line Width(pt)(0 to 5)', default=1, validators=[NumberRange(min=0, max=5, message="Please enter a value in the specified range.")])
	legends = BooleanField('Legends', default=True)
	averaging = IntegerField('Averaging Level(0-10)', default=0, validators=[NumberRange(min=0, max=10, message="Please enter a value in the specified range.")])
	# fps=IntegerField('FPS(Frames per Second)(1-30)', default=12, validators=[NumberRange(min=1, max=30, message="Please enter a value in the specified range.")])
	generate = SubmitField('Generate Graph')
	# generate_anim= SubmitField('Generate Animation')

class AnimForm(FlaskForm):
	countries = SelectMultipleField('Select Countries', choices=country_choices, validators=[DataRequired()])
	start_date = DateField('Start Date(dd-mm-yy)', format='%d-%m-%y', default=first_date, validators=[DataRequired()])#validators
	end_date = DateField('End Date(dd-mm-yy)', format='%d-%m-%y', default=last_date, validators=[DataRequired()])
	x_field	= SelectField('X Axis Data', choices=x_data_choices, default='days')
	y_field = SelectField('Y Axis Data', choices=y_data_choices)
	x_scale = SelectField('X Axis Scale', choices=scale_choices, default='linear')
	y_scale = SelectField('Y Axis Scale', choices=scale_choices, default='linear')
	line_width = FloatField('Line Width(pt)(0 to 5)', default=1, validators=[NumberRange(min=0, max=5, message="Please enter a value in the specified range.")])
	legends = BooleanField('Legends', default=True)
	averaging = IntegerField('Averaging Level(0-10)', default=0, validators=[NumberRange(min=0, max=10, message="Please enter a value in the specified range.")])
	fps=IntegerField('FPS(Frames per Second)(1-30)', default=12, validators=[NumberRange(min=1, max=30, message="Please enter a value in the specified range.")])
	# generate = SubmitField('Generate Graph')
	generate_anim= SubmitField('Generate Animation')

class MessageForm(FlaskForm):
	name=StringField('Name', render_kw={"placeholder": "John Smith"})
	email=StringField('E-Mail Address', render_kw={"placeholder": "johnsmith@xyz.com"}, validators=[DataRequired(), Email(message='Please enter a valid E-mail Address')])
	message=TextAreaField('Message', render_kw={"placeholder": "Your Message"}, validators=[DataRequired()])
	send=SubmitField('Send Message')
