from flask import render_template, flash, redirect, url_for, request
from webapp import app
from webapp.forms import GraphForm, AnimForm, MessageForm
# import webapp.forms as forms_module
from webapp.covid19 import *
import datetime as dt
from webapp.plots_module import Plot as pt
import os
from webapp.email import send_email
# import urllib.request
from webapp.redis_thread import set_var, incr_var, get_var
# from urllib2 import Request, urlopen


countries=list(Recovered.dict.keys());
counter='counter'
res_url=''
http_headers=None
render_id='desktop'
def poll_func():
	global http_headers
	global render_id
	user_device='default'


	try:
		http_headers=dict(request.headers)
		try:
			user_agent=str(http_headers['User-Agent'])
			# print(user_agent)
			if 'iPhone' in user_agent:
				user_device='ios'
			elif 'Android' in user_agent:
				user_device='android'
			elif 'Macintosh' in user_agent:
				user_device='mac'
			elif 'Windows' in user_agent:
				user_device='windows'
			elif 'Ubuntu' in user_agent:
				user_device='linux'
			else:
				user_device='default'
			# print(user_device)
		except:
			print("Couldn't obtain user agent!")
			user_device='default'
	except:
		print("Couldn't obtain headers!")

	
		

	if user_device=='ios' or user_device=='android':
		render_id='mobile'
	else:
		render_id='desktop'



	if os.path.exists(res_url):
		os.remove(res_url)



@app.route('/', methods=['GET', 'Post'])
@app.route('/index', methods=['GET', 'Post'])
def index():
	global res_url


	poll_func()


	incr_var(counter)


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

		
		pt_obj=pt()
		t=pt_obj.generate_plot()
		url="static/img/graph"+str(t)+".png"
		res_url="webapp/"+url
		flash("Graph Generated.")
		return render_template('graph.html', url=url, page='index')
	return render_template('index.html', title='Home', form=graph_form, page='index', render_id=render_id)



@app.route('/animation', methods=['GET', 'POST'])
def animation():
	global res_url
	poll_func()
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

		
		pt_obj=pt()
		t=pt_obj.generate_anim()
		url="static/vid/anim"+str(t)+".mp4"
		res_url="webapp/"+url
		flash("Animation Generated")
		return render_template('anim.html', url=url, page='animation')
	return render_template('animation.html', title='Animation', form=graph_form, page='animation', render_id=render_id)


@app.route('/about')
def about():
	poll_func()
	return render_template('about.html', page='about')


@app.route('/contact', methods=['GET', 'Post'])
def contact():
	poll_func()
	form=MessageForm()
	if form.validate_on_submit():
		print(form.name.data)
		print(form.email.data)
		print(form.message.data)


		#to form filler
		send_email('Raj Covid-19 Grapher - Thank you for your feedback!',
               sender=app.config['ADMINS'][0],
               recipients=[form.email.data],
               text_body=render_template('email/contact_auto_reply.txt', form=form),
               html_body=render_template('email/contact_auto_reply.html', form=form))

		#to admin
		send_email('Raj Covid-19 Grapher Contact Form Filled - '+str(form.email.data),
               sender=app.config['MAIL_USERNAME'],
               recipients=app.config['ADMINS'],
               text_body=render_template('email/contact_msg.txt', form=form),
               html_body=render_template('email/contact_msg.html', form=form))
		return render_template('sent.html', page='contact')
	return render_template('contact.html', page='contact', form=form)


@app.route('/test')
def test():
	poll_func()
	print(dict(request.headers))
	# http_req=request.headers['X-Wap-Profile']
	# http_req=request.headers['X-Wap-Profile']
	
	
	
	
	
	return render_template('test.html', page='test')


@app.route('/hits')
def hits():
	poll_func()
	count=0	
	try:
		count=str(get_var(counter))
		i1=count.find("'")
		i2=count.find("'", i1+1)
		count=count[i1+1:i2]
	except:
		print("Counter redis server unreachable!")

	return render_template('hits.html',page='hits', count=count)

@app.route('/reset_hits')
def reset_hits():
	poll_func()
	set_var(counter,0)
	count='Counter Reset!'
	return render_template('hits.html',page='hits', count=count)



@app.errorhandler(404)
def not_found_error(error):
	poll_func()
	# send_email("404 detected on site", "LOL", "<h1></h1>")
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	poll_func()
	return render_template('500.html'), 500