import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #Mail creds
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['aniansh@yahoo.com']
	# MAIL_SERVER='smtp.googlemail.com'
	# MAIL_PORT=587
	# MAIL_USE_TLS=1
	# MAIL_USERNAME='raj.covid.19.grapher@gmail.com'
	# MAIL_PASSWORD='1-Universe'