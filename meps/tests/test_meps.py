# -*- coding: utf-8 -*-
"""
    MEPS Tests
    ----------

    Tests the MEPS capability to send emails and failover to alternate mail
    providers.
"""

import flask
import json
import pytest
import requests

from mock import Mock

from context import meps


class TestValidProvider:

    def send_email(self, mail):
        return requests.codes['ok']


class TestInvalidProvider:

    def send_email(self, mail):
        return requests.codes['request_timeout']


# Add mock get_mail_providers
meps.get_mail_providers = Mock(return_value=[TestValidProvider()])


@pytest.fixture
def client():
    meps.app.config['TESTING'] = True
    client = meps.app.test_client()

    return client


def client_send_email(mail):
    return client().post('/email', data=mail, content_type='application/json')


def test_valid_email(client):
    valid_mail = json.dumps({
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    })
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_email(client):
    valid_mail = json.dumps({
        'to': 'toATexample.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'body': 'Hello World!',
    })
    response = client_send_email(valid_mail)

    assert response.status_code == requests.codes['bad_request']


def test_invalid_mail_provider(client):
    meps.get_mail_providers = Mock(return_value=[TestInvalidProvider()])

    valid_mail = json.dumps({
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    })
    response = client_send_email(valid_mail)

    assert response.data == ('All mail providers errored when sending mail. '
        'Returning most recent status code.')
    assert response.status_code == requests.codes['request_timeout']


def test_valid_and_invalid_mail_provider(client):
    meps.get_mail_providers = Mock(return_value=[TestValidProvider(), TestInvalidProvider()])

    valid_mail = json.dumps({
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    })
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']


def test_invalid_and_valid_mail_provider(client):
    meps.get_mail_providers = Mock(return_value=[TestInvalidProvider(), TestValidProvider()])

    valid_mail = json.dumps({
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    })
    response = client_send_email(valid_mail)

    assert response.data == 'Mail sent successfully!'
    assert response.status_code == requests.codes['ok']
