# -*- coding: utf-8 -*-
"""
    Mail Provider tests
    ----------

    Tests the email provider and ensures that the MEPS config has the correct
    parameters.
"""
import pytest

from context import email_provider_loader
from context import email_providers
from email_provider_loader import email_provider_loader
from email_providers.mailgun_provider import MailgunProvider


def get_valid_config():
    return {
        'default_email_provider': 'MailgunProvider',
        'mailgun_provider_api_key': 'test_emailgun_api_key',
    }


def test_valid_config_load():
    test_email_provider_loader = email_provider_loader.EmailProviderLoader(
        get_valid_config())
    providers = test_email_provider_loader.get_providers()

    # Test that we have at least 1 email provider
    assert len(providers) > 0
    # Test that default email provider is MailgunProvider
    assert isinstance(providers[0], MailgunProvider)


def test_missing_default_email_provider_config_load():
    valid_config = get_valid_config()
    del valid_config['default_email_provider']
    test_email_provider_loader = email_provider_loader.EmailProviderLoader(
        valid_config)
    providers = test_email_provider_loader.get_providers()

    # Test that we have at least 1 email provider
    assert len(providers) > 0


def test_missing_api_key_error():
    invalid_config = get_valid_config()
    del invalid_config['mailgun_provider_api_key']

    with pytest.raises(email_provider_loader.MissingApiKeyError):
        test_email_provider_loader = email_provider_loader.EmailProviderLoader(
            invalid_config)


def test_unsupported_email_provider_error():
    invalid_config = get_valid_config()
    invalid_config['default_email_provider'] = 'UnsupportedMailProvider'

    with pytest.raises(email_provider_loader.UnsupportedEmailProviderError):
        test_email_provider_loader = email_provider_loader.EmailProviderLoader(
            invalid_config)
