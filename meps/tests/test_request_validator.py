# -*- coding: utf-8 -*-
"""
    Request Validator Tests
    ----------

    Tests the request validator and ensures its behavior on valid and invalid
    email forms.
"""
from context import request_validator
from request_validator import request_validator


def get_valid_email():
    return {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }


def test_valid_email():
    assert request_validator.validate_email_request(get_valid_email())


def test_missing_to():
    invalid_email = get_valid_email()
    del invalid_email['to']

    assert not request_validator.validate_email_request(invalid_email)


def test_missing_to_name():
    invalid_email = get_valid_email()
    del invalid_email['to_name']

    assert not request_validator.validate_email_request(invalid_email)


def test_missing_from():
    invalid_email = get_valid_email()
    del invalid_email['from']

    assert not request_validator.validate_email_request(invalid_email)


def test_missing_from_name():
    invalid_email = get_valid_email()
    del invalid_email['from_name']

    assert not request_validator.validate_email_request(invalid_email)


def test_missing_subject():
    invalid_email = get_valid_email()
    del invalid_email['subject']

    assert not request_validator.validate_email_request(invalid_email)


def test_missing_body():
    invalid_email = get_valid_email()
    del invalid_email['body']

    assert not request_validator.validate_email_request(invalid_email)


def test_invalid_to_email():
    invalid_email = get_valid_email()
    invalid_email['to'] = 'toATexample.com'

    assert not request_validator.validate_email_request(invalid_email)


def test_invalid_from_email():
    invalid_email = get_valid_email()
    invalid_email['from'] = 'fromATexample.com'

    assert not request_validator.validate_email_request(invalid_email)
