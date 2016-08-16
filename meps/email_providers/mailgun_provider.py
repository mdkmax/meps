# -*- coding: utf-8 -*-
"""
    Mailgun Provider
    ----------

    Sends email to the Mailgun API endpoint.
"""
import requests
from requests.exceptions import ConnectionError, HTTPError


class MailgunProvider:

    def __init__(self, api_key):
        self._api_key = api_key

    def send_email(self, email):
        """Sends email to the Mailgun API endpoint.

        Args:
            email: A dictionary containing the email request

        Returns:
            An HTTP status code from the Mailgun response. If the Mailgun
            response times out and results in a ConnectionError, then returns
            the HTTP status code for request timeout.
        """
        try:
            response = requests.post(
                'https://api.mailgun.net/v3/sandbox18b60def035c45ad9499441c9e34'
                '9853.mailgun.org/messages',
                auth=('api', self._api_key),
                data={'from': '{} <{}>'.format(email['from_name'], email['from']),
                      'to': ['{} <{}>'.format(email['to_name'], email['to'])],
                      'subject': email['subject'],
                      'text': email['body']})
            return response.status_code
        except ConnectionError:
            return requests.codes['request_timeout']
