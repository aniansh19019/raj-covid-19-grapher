from flask import render_template, flash, redirect, url_for
from webapp import app
from webapp.forms import LoginForm, GraphForm, AnimForm, MessageForm
from webapp.covid19 import *
import datetime as dt
from webapp.plots_module import Plot as pt
import os
from webapp.email import send_email
countries=list(Recovered.dict.keys());


@app.route('/', methods=['GET', 'Post'])
@app.route('/index', methods=['GET', 'Post'])
def index():
	# print(os.getcwd())
	graph_form = GraphForm()
	if graph_form.validate_on_submit():
		# print(graph_form.countries.data)
		pt.countries=graph_form.countries.data
		pt.start=Confirmed.obj_to_str(graph_form.start_date.data)
		pt.end=Confirmed.obj_to_str(graph_form.end_date.data)
		pt.x_field=graph_form.x_field.data
		pt.y_field=graph_form.y_field.data
		pt.xplot_scale=graph_form.x_scale.data
		pt.yplot_scale=graph_form.y_scale.data
		pt.line_width=graph_form.line_width.data
		pt.leg=graph_form.legends.data
		pt.smoothness=graph_form.averaging.data

		flash("Graph Generated.")
		pt_obj=pt()
		t=pt_obj.generate_plot()
		url="webapp/static/img/graph"+str(t)+".png"
		return render_template('graph.html', url=url, page='index')
	return render_template('index.html', title='Home', form=graph_form, page='index')



@app.route('/animation', methods=['GET', 'POST'])
def animation():
	graph_form = AnimForm()
	if graph_form.validate_on_submit():
		# print(graph_form.countries.data)
		# return render_template('animation.html', title='Animation', form=graph_form, page='animation', submit=True)
		pt.countries=graph_form.countries.data
		pt.start=Confirmed.obj_to_str(graph_form.start_date.data)
		pt.end=Confirmed.obj_to_str(graph_form.end_date.data)
		pt.x_field=graph_form.x_field.data
		pt.y_field=graph_form.y_field.data
		pt.xplot_scale=graph_form.x_scale.data
		pt.yplot_scale=graph_form.y_scale.data
		pt.line_width=graph_form.line_width.data
		pt.leg=graph_form.legends.data
		pt.smoothness=graph_form.averaging.data
		pt.fps=graph_form.fps.data

		flash("Animation Generated")
		pt_obj=pt()
		t=pt_obj.generate_anim()
		url="webapp/static/vid/anim"+str(t)+".mp4"
		return render_template('anim.html', url=url, page='animation')
	return render_template('animation.html', title='Animation', form=graph_form, page='animation')


@app.route('/about')
def about():
	return render_template('about.html', page='about')


@app.route('/contact', methods=['GET', 'Post'])
def contact():
	form=MessageForm()
	if form.validate_on_submit():
		print(form.name.data)
		print(form.email.data)
		print(form.message.data)
		return render_template('sent.html', page='contact')
	return render_template('contact.html', page='contact', form=form)


@app.route('/more_apps')
def more_apps():
	return render_template('more_apps.html', page='more_apps')


@app.errorhandler(404)
def not_found_error(error):
	# send_email("404 detected on site", "LOL", "<h1></h1>")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500