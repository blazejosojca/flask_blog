from flask import render_template
from app import app
from flask_mail import Message
from app import mail


def send_mail(subject, sender, recipients, test_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = test_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('Blog Reset Your Password',
              sender=app.config['ADMINS'][1],
              recipients=[user.email],
              test_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password.html',
                                        user=user, token=token))
