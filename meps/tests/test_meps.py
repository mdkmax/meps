# -*- coding: utf-8 -*-
"""
    MEPS Tests
    ----------

    Tests the MEPS capability to send emails and failover to alternate mail
    providers.
"""

import json
import pytest
import requests

from mock import Mock, patch

from context import meps


class TestValidProvider:

    def send_email(self, mail):
        return requests.codes['ok']


class TestInvalidProvider:

    def send_email(self, mail):
        return requests.codes['request_timeout']


@pytest.fixture
def client():
    meps.app.config['TESTING'] = True
    client = meps.app.test_client()

    return client


def client_send_email(mail):
    return client().post('/email', data=mail, content_type='application/json')


def get_valid_mail():
    return {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }


def test_valid_email(client):
    # Add mock get_mail_providers
    meps.get_mail_providers = Mock(return_value=[TestValidProvider()])

    valid_mail = json.dumps(get_valid_mail())
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_email(client):
    meps.get_mail_providers = Mock(return_value=[TestValidProvider()])

    valid_mail = get_valid_mail()
    valid_mail['to'] = 'toATexample.com'
    valid_mail = json.dumps(valid_mail)
    response = client_send_email(valid_mail)

    assert response.status_code == requests.codes['bad_request']


def test_invalid_mail_provider(client):
    meps.get_mail_providers = Mock(return_value=[TestInvalidProvider()])

    valid_mail = json.dumps(get_valid_mail())
    response = client_send_email(valid_mail)

    assert response.data == ('All mail providers errored when sending mail. '
                             'Returning most recent status code.')
    assert response.status_code == requests.codes['request_timeout']


def test_valid_and_invalid_mail_provider(client):
    meps.get_mail_providers = Mock(
        return_value=[TestValidProvider(), TestInvalidProvider()])

    valid_mail = json.dumps(get_valid_mail())
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_and_valid_mail_provider(client):
    meps.get_mail_providers = Mock(
        return_value=[TestInvalidProvider(), TestValidProvider()])

    valid_mail = json.dumps(get_valid_mail())
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_many_mail_providers(client):
    mail_providers = []

    # Append 9 invalid test providers
    for i in xrange(0, 9):
        mail_providers.append(TestInvalidProvider())

    mail_providers.append(TestValidProvider())

    meps.get_mail_providers = Mock(return_value=mail_providers)

    valid_mail = json.dumps(get_valid_mail())
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


@patch.object(TestValidProvider, 'send_email')
def test_html_tags_stripped(client):
    test_valid_provider = TestValidProvider()
    meps.get_mail_providers = Mock(return_value=[test_valid_provider])

    valid_mail = get_valid_mail()
    valid_mail['body'] = '<div><p>Hello</p><p>World!</p></div>'
    valid_mail = json.dumps(valid_mail)
    response = client_send_email(valid_mail)

    expected_mail = get_valid_mail()
    expected_mail['body'] = 'HelloWorld!'

    test_valid_provider.send_email.assert_called_with(expected_mail)
