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

from mail_provider_loader.mail_provider_loader import MailProviderLoader
from request_validator import request_validator


app = Flask(__name__)


def get_mail_providers():
    """Instantiate mail providers as needed per request on the Flask global object.

    Returns:
        A list of mail provider instances.
    """
    if not hasattr(g, 'mail_providers'):
        with open('meps_config.json') as config_file:
            config = json.load(config_file)

            # Instantiate all mail providers.
            mail_provider = MailProviderLoader(config)
            g.mail_providers = mail_provider.get_providers()

    return g.mail_providers


@app.route('/', methods=['POST'])
def redirect_to_send_email():
    """Send error message in case someone tries to POST to root.

    Returns:
        A tuple containing an error message followed by the HTTP code 405 for
        not allowed requests.
    """
    error_message = 'Please send email to {}'.format(request.url + 'email')
    return error_message, requests.codes['not_allowed']


@app.route('/email', methods=['POST'])
def send_email():
    """Sends email to the list of mail providers.

    Iterates through a list of mail providers and attempts to send the given
    mail through each one. Returns a success message and error code on the first
    successful send. Otherwise, iterates through all mail providers and returns
    an error message with the status code of the last mail provider send
    request.

    Returns:
        A tuple containing the request status message followed by the status
        code.
    """
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
