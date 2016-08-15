# -*- coding: utf-8 -*-
"""
    Mail Provider tests
    ----------

    Tests the mail provider and ensures that the MEPS config has the correct
    parameters.
"""
import pytest

from context import mail_provider_loader
from context import mail_providers
from mail_provider_loader import mail_provider_loader
from mail_providers.mailgun_provider import MailgunProvider


def get_valid_config():
    return {
        'default_mail_provider': 'MailgunProvider',
        'mailgun_provider_api_key': 'test_mailgun_api_key',
    }


def test_valid_config_load():
    test_mail_provider_loader = mail_provider_loader.MailProviderLoader(
        get_valid_config())
    providers = test_mail_provider_loader.get_providers()

    # Test that we have at least 1 mail provider
    assert len(providers) > 0
    # Test that default mail provider is MailgunProvider
    assert isinstance(providers[0], MailgunProvider)


def test_missing_default_mail_provider_config_load():
    valid_config = get_valid_config()
    del valid_config['default_mail_provider']
    test_mail_provider_loader = mail_provider_loader.MailProviderLoader(
        valid_config)
    providers = test_mail_provider_loader.get_providers()

    # Test that we have at least 1 mail provider
    assert len(providers) > 0


def test_missing_api_key_error():
    invalid_config = get_valid_config()
    del invalid_config['mailgun_provider_api_key']

    with pytest.raises(mail_provider_loader.MissingApiKeyError):
        test_mail_provider_loader = mail_provider_loader.MailProviderLoader(
            invalid_config)


def test_unsupported_mail_provider_error():
    invalid_config = get_valid_config()
    invalid_config['default_mail_provider'] = 'UnsupportedMailProvider'

    with pytest.raises(mail_provider_loader.UnsupportedMailProviderError):
        test_mail_provider_loader = mail_provider_loader.MailProviderLoader(
            invalid_config)
