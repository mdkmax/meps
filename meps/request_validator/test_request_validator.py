import pytest

from request_validator import validate_mail_request


def test_valid_mail():
    valid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert validate_mail_request(valid_mail)


def test_missing_to():
    invalid_mail = {
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_missing_to_name():
    invalid_mail = {
        'to': 'to@example.com',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_missing_from():
    invalid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_missing_from_name():
    invalid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_missing_subject():
    invalid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_missing_body():
    invalid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
    }

    assert not validate_mail_request(invalid_mail)


def test_invalid_to_email():
    invalid_mail = {
        'to': 'toATexample.com',
        'to_name': 'Jane Doe',
        'from': 'from@example.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)


def test_invalid_from_email():
    invalid_mail = {
        'to': 'to@example.com',
        'to_name': 'Jane Doe',
        'from': 'fromATexample.com',
        'from_name': 'John Smith',
        'subject': 'Test',
        'body': 'Hello World!',
    }

    assert not validate_mail_request(invalid_mail)
