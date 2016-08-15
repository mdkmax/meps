# -*- coding: utf-8 -*-
"""
    Multiple Email Providers Service (MEPS)
    ------------------------------
    A service that validations email POST requests and forwards them to
    available mail services that are specified in configurations.

"""

import requests

from bs4 import BeautifulSoup
from flask import abort, Flask, g, json, redirect, request, url_for

from mail_provider_loader import MailProviderLoader
from request_validator import request_validator


app = Flask(__name__)


@app.before_request
def before_request():
    g.mail_providers = get_mail_providers()


def get_mail_providers():
    if not hasattr(g, 'mail_providers'):
        with open('meps_config.json') as config_file:
            config = json.load(config_file)

            # Instantiate all mail providers.
            mail_provider = MailProviderLoader(config)
            g.mail_providers = mail_provider.get_providers()

    return g.mail_providers


# Add error message in case someone tries to POST to root.
@app.route('/', methods=['POST'])
def redirect_to_send_email():
    error_message = 'Please send email to {}'.format(request.url + 'email')
    return error_message, requests.codes['not_allowed']


@app.route('/email', methods=['POST'])
def send_email():
    if request.headers['Content-Type'] != 'application/json':
        abort(requests.codes['bad_request'])

    mail = request.json

    # Strip all HTML tags.
    mail['body'] = BeautifulSoup(mail['body'], 'html.parser').get_text()

    if not request_validator.validate_mail_request(mail):
        abort(requests.codes['bad_request'])

    mail_providers = get_mail_providers()

    for mail_provider in mail_providers:
        status_code = mail_provider.send_email(mail)

        if status_code == requests.codes['ok']:
            return 'Mail sent successfully!', status_code

    error_message = ('All mail providers errored when sending mail. Returning '
                     'most recent status code.')

    return error_message, status_code
