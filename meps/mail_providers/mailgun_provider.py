import requests
from requests.exceptions import ConnectionError, HTTPError


class MailgunProvider:

    def __init__(self, api_key):
        self._api_key = api_key

    def send_email(self, mail):
        try:
            response = requests.post(
                'https://api.mailgun.net/v3/sandbox18b60def035c45ad9499441c9e34'
                '9853.mailgun.org/messages',
                auth=('api', self._api_key),
                data={'from': '{} <{}>'.format(mail['from_name'], mail['from']),
                      'to': ['{} <{}>'.format(mail['to_name'], mail['to'])],
                      'subject': mail['subject'],
                      'text': mail['body']})
            return response.status_code
        except ConnectionError:
            return requests.codes['request_timeout']
