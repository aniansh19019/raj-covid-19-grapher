from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)

mail = Mail(app)
bootstrap = Bootstrap(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config.from_object(Config)
from webapp import routes