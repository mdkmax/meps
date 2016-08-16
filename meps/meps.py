# -*- coding: utf-8 -*-
"""
    Multiple Email Providers Service (MEPS)
    ------------------------------
    A service that validations email POST requests and forwards them to
    available email services that are specified in configurations.

"""

import requests

from bs4 import BeautifulSoup
from flask import abort, Flask, g, json, redirect, request, url_for

from email_provider_loader.email_provider_loader import EmailProviderLoader
from request_validator import request_validator


app = Flask(__name__)


def get_email_providers():
    """Instantiate email providers as needed.

    Returns:
        A list of email provider instances.
    """
    if not hasattr(g, 'email_providers'):
        with open('meps/meps_config.json') as config_file:
            config = json.load(config_file)

            # Instantiate all email providers.
            email_provider = EmailProviderLoader(config)
            g.email_providers = email_provider.get_providers()

    return g.email_providers


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
    """Sends email to the list of email providers.

    Iterates through a list of email providers and attempts to send the given
    email through each one. Returns a success message and error code on the
    first successful send. Otherwise, iterates through all email providers and
    returns an error message with the status code of the last email provider
    send request.

    Returns:
        A tuple containing the request status message followed by the status
        code.
    """
    if request.headers['Content-Type'] != 'application/json':
        abort(requests.codes['bad_request'])

    email = request.json

    # Strip all HTML tags.
    email['body'] = BeautifulSoup(email['body'], 'html.parser').get_text()

    if not request_validator.validate_email_request(email):
        abort(requests.codes['bad_request'])

    email_providers = get_email_providers()

    for email_provider in email_providers:
        status_code = email_provider.send_email(email)

        if status_code == requests.codes['ok']:
            return 'Mail sent successfully!', status_code

    error_message = ('All email providers errored when sending email. '
                     'Returning most recent status code.')

    return error_message, status_code
