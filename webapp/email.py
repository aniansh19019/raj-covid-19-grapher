from flask_mail import Message
from webapp import mail

def send_email(subject, text_body, html_body):
    msg = Message(subject, sender='raj.covid.19.grapher@gmail.com', recipients=['aniansh@yahoo.com'])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)