#!/usr/bin/env

"""
Former2

    Ondrej Sika <ondrej@ondrejsika.com>
    https://gitlab.sikahq.com/ondrej/former2
    https://github.com/former2/former2

Simple form backend for static sites.
"""

import argparse
import smtplib

from werkzeug import MultiDict
from flask import Flask, redirect, request
from flask_mail import Mail, Message


root_parser = argparse.ArgumentParser()
root_parser.add_argument('--host', default='0.0.0.0')
root_parser.add_argument('--port', type=int, default=80)
root_parser.add_argument('--debug', action='store_true')
root_parser.add_argument('--smtp-server', required=True)
root_parser.add_argument('--smtp-port', required=True, type=int)
root_parser.add_argument('--smtp-tls', action='store_true')
root_parser.add_argument('--smtp-ssl', action='store_true')
root_parser.add_argument('--smtp-username', required=True)
root_parser.add_argument('--smtp-password', required=True)
root_parser.add_argument('--smtp-email', required=True)
root_parser.add_argument('--notify-to', required=True)

args = root_parser.parse_args()

app = Flask(__name__)
app.config['MAIL_SERVER'] = args.smtp_server
app.config['MAIL_PORT'] = args.smtp_port
app.config['MAIL_USERNAME'] = args.smtp_username
app.config['MAIL_PASSWORD'] = args.smtp_password
app.config['MAIL_USE_TLS'] = args.smtp_tls
app.config['MAIL_USE_SSL'] = args.smtp_ssl

mail = Mail(app)

@app.route('/')
def index():
    return 'former2'

@app.route('/form', methods=['GET', 'POST'])
def form():
    data = MultiDict()
    data.update(request.args)
    data.update(request.form)

    form_name = data.get('_form_name')
    redirect_url = data.get('_redirect_url')

    body = []
    for key, val in data.items():
        body.append('%s: %s' % (key, val))
        body.append('')
    body.append('')
    body.append('--')
    body.append('sent form former2 by Ondrej Sika')
    body.append('https://github.com/former2/former2')

    if form_name:
        subject = '[former2] Submit notification from %s' % form_name
    else:
        subject = '[former2] Submit notification'

    message = Message(subject,
                  sender=args.smtp_email,
                  recipients=args.notify_to.split(','))
    
    message.body = '\n'.join(body)
    mail.send(message)

    if redirect_url:
        return redirect(redirect_url)
    else:
        return message.body.replace('\n','\n<br>')

app.debug = args.debug
app.run(host=args.host, port=args.port)
