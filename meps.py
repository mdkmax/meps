# -*- coding: utf-8 -*-
"""
    Multiple Email Providers Service (MEPS)
    ------------------------------
    A service that validations email POST requests and forwards them to
    available mail services that are specified in configurations.

"""

import requests

from bs4 import BeautifulSoup
from flask import Flask, request, session, g, redirect, url_for, abort, \
     flash, json

from mail_provider_loader import MailProviderLoader
from request_validator import validate_mail_request


app = Flask(__name__)


def get_mail_providers():
    if not hasattr(g, 'mail_providers'):
        with open('meps_config.json') as config_file:
            config = json.load(config_file)

            # Instantiate all mail providers.
            mail_provider = MailProviderLoader(config)
            g.mail_providers = mail_provider.get_providers()

    return g.mail_providers


@app.route('/email', methods=['POST'])
def send_email():
    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    mail = request.json

    #Strip all HTML tags.
    mail['body'] = BeautifulSoup(mail['body'], 'html.parser').get_text()

    if not validate_mail_request(mail):
        abort(400)

    for mail_provider in get_mail_providers():
        result, status_code = mail_provider.send_email(mail)

        if status_code == 200:
            return 'Mail sent successfully!', status_code

    return ('All mail providers errored when sending mail. Returning most '
        'recent status code.'), status_code