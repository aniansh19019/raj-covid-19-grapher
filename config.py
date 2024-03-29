import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #Mail creds_URL
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['aniansh@yahoo.com']


	#redis
	REDIS_URL = os.environ.get("REDIS_URL") 
	#sqlAlchemy

	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        # 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI="postgres://spfqwjelmjhvrk:39918804fa6bb6546ea08339b2c26936fed481e921a3cc70b189db8f2405fb00@ec2-46-137-84-173.eu-west-1.compute.amazonaws.com:5432/d6dsbce81tcuqm"
	#server vars
	
	# REDIS_URL = "redis://h:pe4ba8bd95cc576bb4853d7660e60cc818c1f45b6023b59061250a42a5ebed4fb@ec2-52-213-23-142.eu-west-1.compute.amazonaws.com:16569"
	# REDIS_URL='redis://h:p25240e9fa48c1a3a2a3fa86a3071e100fb2c1a1053f05b08f0ee03aed02b5e88@ec2-18-207-83-208.compute-1.amazonaws.com:19439'
	# MAIL_SERVER='smtp.googlemail.com'
	# MAIL_PORT=587
	# MAIL_USE_TLS=1
	# MAIL_USERNAME='raj.covid.19.grapher@gmail.com'
	# MAIL_PASSWORD='1-Universe'