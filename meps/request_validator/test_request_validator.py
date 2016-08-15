# -*- coding: utf-8 -*-
"""
    Request Validator Tests
    ----------

    Tests the request validator and ensures its behavior on valid and invalid
    email forms.
"""
from request_validator import validate_mail_request


def get_valid_mail():
    return {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }


def test_valid_mail():
    assert validate_mail_request(get_valid_mail())


def test_missing_to():
    invalid_mail = get_valid_mail()
    del invalid_mail['to']

    assert not validate_mail_request(invalid_mail)


def test_missing_to_name():
    invalid_mail = get_valid_mail()
    del invalid_mail['to_name']

    assert not validate_mail_request(invalid_mail)


def test_missing_from():
    invalid_mail = get_valid_mail()
    del invalid_mail['from']

    assert not validate_mail_request(invalid_mail)


def test_missing_from_name():
    invalid_mail = get_valid_mail()
    del invalid_mail['from_name']

    assert not validate_mail_request(invalid_mail)


def test_missing_subject():
    invalid_mail = get_valid_mail()
    del invalid_mail['subject']

    assert not validate_mail_request(invalid_mail)


def test_missing_body():
    invalid_mail = get_valid_mail()
    del invalid_mail['body']

    assert not validate_mail_request(invalid_mail)


def test_invalid_to_email():
    invalid_mail = get_valid_mail()
    invalid_mail['to'] = 'toATexample.com'

    assert not validate_mail_request(invalid_mail)


def test_invalid_from_email():
    invalid_mail = get_valid_mail()
    invalid_mail['from'] = 'fromATexample.com'

    assert not validate_mail_request(invalid_mail)
