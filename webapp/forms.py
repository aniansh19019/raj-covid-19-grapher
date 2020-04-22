from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, SelectMultipleField, FloatField, IntegerField, TextAreaField
# from wtforms import *
from wtforms.validators import *
from wtforms_components import DateRange, If
from wtforms.fields.html5 import DateField

from webapp.covid19 import *
import datetime as dt

from webapp.plots_module import Plot as pt




first_date=Confirmed.str_to_obj(Confirmed.fields[5])
last_date=Confirmed.str_to_obj(Confirmed.latest_date())

first_str=Confirmed.fields[5]
last_str=Confirmed.latest_date()


custom_country_labels={'US':'United States', 'Korea, South':'South Korea'}

alphabetical=list(Confirmed.dict.keys());
sorts=list(Confirmed.dict.keys());


for i in range(len(sorts)-1):
	for j in range(len(sorts)-i-1):
		if(Confirmed.cases(sorts[j],last_str)<Confirmed.cases(sorts[j+1],last_str)):
			temp=sorts[j]
			sorts[j]=sorts[j+1]
			sorts[j+1]=temp

keys=[]

top_n=20


for i in range(top_n):
	keys.append(sorts[i])
	alphabetical.remove(sorts[i])

for key in alphabetical:
	keys.append(key)




country_choices=[]
for key in keys:
	if key in custom_country_labels.keys():
		sub=(key,custom_country_labels[key])
	else:
		sub=(key,key)
	country_choices.append(sub)

default_countries=['US', 'Italy', 'Spain', 'France', 'United Kingdom', 'Korea, South', 'Japan', 'India', 'Pakistan', 'Iran']

scale_choices=[("linear","Linear"), ("log", "Logarithmic")]
x_data_choices=pt.data_keys.copy()
y_data_choices=pt.data_keys.copy()
y_data_choices.pop(0)





def anim_num_validate(form,field):
	if len(form.countries.data)>5:
		raise ValidationError('Please select no more than 5 items!')

def custom_data_required_validate(form,field):
	print(field.data)
	if field.data==[]:
		raise ValidationError('Please select one or more countries!')



def start_validate(form, field):
	if form.start_date.data>form.end_date.data:
		raise ValidationError('Start Date must be less than End Date!')

def end_validate(form, field):
	if form.start_date.data>form.end_date.data:
		raise ValidationError('End Date must be greater than Start Date!')

class GraphForm(FlaskForm):
	countries = SelectMultipleField('Select Countries', render_kw={"id":"multi"}, choices=country_choices, validators=[custom_data_required_validate])
	start_date = DateField('Start Date(dd/mm/yyyy)', 
							format='%Y-%m-%d', 
							default=first_date,
							validators=[DataRequired(), 
									DateRange(max=last_date, min=first_date, message='Date must be between "'+first_date.strftime('%d-%m-%y')+'" and "'+last_date.strftime('%d-%m-%y')+'"'),
									start_validate])#validators

	end_date = DateField('End Date(dd/mm/yyyy)', 
							format='%Y-%m-%d', 
							default=last_date, 
							validators=[DataRequired(), 
							DateRange(max=last_date, min=first_date, message='Date must be between "'+first_date.strftime('%d-%m-%y')+'" and "'+last_date.strftime('%d-%m-%y')+'"'),
							end_validate])
	x_field	= SelectField('X Axis Data', choices=x_data_choices, default='days')
	y_field = SelectField('Y Axis Data', choices=y_data_choices)
	x_scale = SelectField('X Axis Scale', choices=scale_choices, default='linear')
	y_scale = SelectField('Y Axis Scale', choices=scale_choices, default='linear')
	line_width = FloatField('Line Width(pt)(0 to 5)', default=1, validators=[NumberRange(min=0, max=5, message="Please enter a value in the specified range.")])
	averaging = IntegerField('Averaging Level(0-10)', default=0, validators=[NumberRange(min=0, max=10, message="Please enter a value in the specified range.")])
	# fps=IntegerField('FPS(Frames per Second)(1-30)', default=12, validators=[NumberRange(min=1, max=30, message="Please enter a value in the specified range.")])
	legends = BooleanField('Legends', default=True)
	generate = SubmitField('Generate Graph')
	# generate_anim= SubmitField('Generate Animation')


class AnimForm(FlaskForm):
	countries = SelectMultipleField('Select Countries(Maximum 5)', render_kw={"id":"multi"}, choices=country_choices, validators=[custom_data_required_validate, anim_num_validate])
	start_date = DateField('Start Date(dd/mm/yyyy)', 
							format='%Y-%m-%d', 
							default=first_date, 
							validators=[DataRequired(), 
									DateRange(max=last_date, min=first_date, message='Date must be between "'+first_date.strftime('%d-%m-%y')+'" and "'+last_date.strftime('%d-%m-%y')+'"'),
									start_validate])#validators

	end_date = DateField('End Date(dd/mm/yyyy)', 
							format='%Y-%m-%d', 
							default=last_date, 
							validators=[DataRequired(), 
							DateRange(max=last_date, min=first_date, message='Date must be between "'+first_date.strftime('%d-%m-%y')+'" and "'+last_date.strftime('%d-%m-%y')+'"'),
							end_validate])
	x_field	= SelectField('X Axis Data', choices=x_data_choices, default='days')
	y_field = SelectField('Y Axis Data', choices=y_data_choices)
	x_scale = SelectField('X Axis Scale', choices=scale_choices, default='linear')
	y_scale = SelectField('Y Axis Scale', choices=scale_choices, default='linear')
	line_width = FloatField('Line Width(pt)(0 to 5)', default=1, validators=[NumberRange(min=0, max=5, message="Please enter a value in the specified range.")])
	
	averaging = IntegerField('Averaging Level(0-10)', default=0, validators=[NumberRange(min=0, max=10, message="Please enter a value in the specified range.")])
	fps=IntegerField('FPS(Frames per Second)(1-30)', default=12, validators=[NumberRange(min=1, max=30, message="Please enter a value in the specified range.")])
	# generate = SubmitField('Generate Graph')
	legends = BooleanField('Legends', default=True)
	generate_anim= SubmitField('Generate Animation')

class MessageForm(FlaskForm):
	name=StringField('Name', render_kw={"placeholder": "John Smith"})
	email=StringField('E-Mail Address', render_kw={"placeholder": "johnsmith@xyz.com"}, validators=[DataRequired(), Email(message='Please enter a valid E-mail Address')])
	message=TextAreaField('Message', render_kw={"placeholder": "Your Message"}, validators=[DataRequired()])
	send=SubmitField('Send Message')
