# -*- coding: utf-8 -*-
"""
    MEPS Tests
    ----------

    Tests the MEPS capability to send emails and failover to alternate email
    providers.
"""

import json
import pytest
import requests

from mock import Mock, patch

from context import meps


class TestValidProvider:

    def send_email(self, email):
        return requests.codes['ok']


class TestInvalidProvider:

    def send_email(self, email):
        return requests.codes['request_timeout']


@pytest.fixture
def client():
    meps.app.config['TESTING'] = True
    client = meps.app.test_client()

    return client


def client_send_email(email):
    return client().post('/email', data=email, content_type='application/json')


def get_valid_email():
    return {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }


def test_valid_email(client):
    # Add mock get_email_providers
    meps.get_email_providers = Mock(return_value=[TestValidProvider()])

    valid_email = json.dumps(get_valid_email())
    response = client_send_email(valid_email)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_email(client):
    meps.get_email_providers = Mock(return_value=[TestValidProvider()])

    valid_email = get_valid_email()
    valid_email['to'] = 'toATexample.com'
    valid_email = json.dumps(valid_email)
    response = client_send_email(valid_email)

    assert response.status_code == requests.codes['bad_request']


def test_invalid_email_provider(client):
    meps.get_email_providers = Mock(return_value=[TestInvalidProvider()])

    valid_email = json.dumps(get_valid_email())
    response = client_send_email(valid_email)

    assert response.data == ('All email providers errored when sending email. '
                             'Returning most recent status code.')
    assert response.status_code == requests.codes['request_timeout']


def test_valid_and_invalid_email_provider(client):
    meps.get_email_providers = Mock(
        return_value=[TestValidProvider(), TestInvalidProvider()])

    valid_email = json.dumps(get_valid_email())
    response = client_send_email(valid_email)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_and_valid_email_provider(client):
    meps.get_email_providers = Mock(
        return_value=[TestInvalidProvider(), TestValidProvider()])

    valid_email = json.dumps(get_valid_email())
    response = client_send_email(valid_email)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_many_email_providers(client):
    email_providers = []

    # Append 9 invalid test providers
    for i in xrange(0, 9):
        email_providers.append(TestInvalidProvider())

    email_providers.append(TestValidProvider())

    meps.get_email_providers = Mock(return_value=email_providers)

    valid_email = json.dumps(get_valid_email())
    response = client_send_email(valid_email)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


@patch.object(TestValidProvider, 'send_email')
def test_html_tags_stripped(client):
    test_valid_provider = TestValidProvider()
    meps.get_email_providers = Mock(return_value=[test_valid_provider])

    valid_email = get_valid_email()
    valid_email['body'] = '<div><p>Hello</p><p>World!</p></div>'
    valid_email = json.dumps(valid_email)
    response = client_send_email(valid_email)

    expected_email = get_valid_email()
    expected_email['body'] = 'HelloWorld!'

    # Test that the HTML tags were stripped before being the email was sent.
    test_valid_provider.send_email.assert_called_with(expected_email)
