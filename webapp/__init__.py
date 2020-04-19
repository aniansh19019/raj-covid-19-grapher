import logging
from logging.handlers import SMTPHandler
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)


bootstrap = Bootstrap(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config.from_object(Config)



mail = Mail(app)



from webapp import routes



if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Covid-19 Grapher Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        # print("mail sent")
        app.logger.addHandler(mail_handler)