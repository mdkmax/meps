# -*- coding: utf-8 -*-
"""
    Mail Provider Loader
    ------------------------------
    A class that reads from the given config and instantiates the corresponding
    mail providers.

"""
import importlib
import sys
import os

# Add path for mail provider imports.
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from mail_providers.mailgun_provider import MailgunProvider


class Error(Exception):
    pass


class MissingApiKeyError(Error):
    pass


class UnsupportedMailProviderError(Error):
    pass


class MailProviderLoader:

    def __init__(self, config):
        self.providers = self._load_mail_providers(config)

    def _load_mail_providers(self, config):
        """Load mail providers from the given config.

        Instantiates the mail provider specified by the "default_mail_provider"
        parameter in the config. If "default_mail_provider" is not specified,
        then the first mail provider will default to MailgunProvider.

        Args:
            config: A dictionary containing a list of parameters for mail
                providers.

        Returns:
            A list of instances of all mail providers.

        Raises:
            MissingApiKeyError: If the "mailgun_provider_api_key" is not
                provided in the config.
            UnsupportedMailProviderError: If the mail provider specified in
                the "default_mail_provider" is not supported.
        """
        if 'mailgun_provider_api_key' not in config:
            raise MissingApiKeyError

        default_mail_provider = config.get(
            'default_mail_provider', 'MailgunProvider')

        providers = []

        if default_mail_provider == 'MailgunProvider':
            providers.append(MailgunProvider(
                config['mailgun_provider_api_key']))
        else:
            # Mailgun is currently the only supported mail provider.
            raise UnsupportedMailProviderError

        return providers

    def get_providers(self):
        return self.providers
