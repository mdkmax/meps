# -*- coding: utf-8 -*-
"""
    Mail Provider Loader
    ------------------------------
    A class that reads from the given config and instantiates the corresponding
    email providers.

"""
import importlib
import sys
import os

# Add path for email provider imports.
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from email_providers.mailgun_provider import MailgunProvider


class Error(Exception):
    pass


class MissingApiKeyError(Error):
    pass


class UnsupportedEmailProviderError(Error):
    pass


class EmailProviderLoader:

    def __init__(self, config):
        self.providers = self._load_email_providers(config)

    def _load_email_providers(self, config):
        """Load email providers from the given config.

        Instantiates the email provider specified by the
        'default_email_provider' parameter in the config. If
        'default_email_provider' is not specified, then the first email provider
        will default to MailgunProvider.

        Args:
            config: A dictionary containing a list of parameters for email
                providers.

        Returns:
            A list of instances of all email providers.

        Raises:
            MissingApiKeyError: If the 'mailgun_provider_api_key' is not
                provided in the config.
            UnsupportedMailProviderError: If the email provider specified in
                the 'default_email_provider' is not supported.
        """
        if 'mailgun_provider_api_key' not in config:
            raise MissingApiKeyError

        default_email_provider = config.get(
            'default_email_provider', 'MailgunProvider')

        providers = []

        if default_email_provider == 'MailgunProvider':
            providers.append(MailgunProvider(
                config['mailgun_provider_api_key']))
        else:
            # Mailgun is currently the only supported email provider.
            raise UnsupportedEmailProviderError

        return providers

    def get_providers(self):
        return self.providers
