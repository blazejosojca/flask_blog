from flask import render_template, current_app
from flask_mail import Message
from flask_babel import _
from app import mail

from threading import Thread

import smtplib
import ssl


def send_async_email(current_app, msg):
    with current_app.app_context():
        mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    port = current_app.load_json['MAIL_PORT']
    password = current_app.load_json['MAIL_PASSWORD']
    smtp_server = current_app.load_json['MAIL_SERVER']
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.body)

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail(_('Blog Reset Your Password'),
              sender=current_app.load_json['ADMINS'][0],
              recipients=[user.email],
              text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password.html',
                                        user=user, token=token))
