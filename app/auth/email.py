from flask import render_template, current_app
from flask_mail import Message
import smtplib
import ssl


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    port = current_app.config['MAIL_PORT']
    password = current_app.config['MAIL_PASSWORD']
    smtp_server = current_app.config['MAIL_SERVER']
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.body)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('Blog Reset Your Password',
              sender=current_app.config['ADMINS'][0],
              recipients=[user.email],
              text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password.html',
                                        user=user, token=token))
