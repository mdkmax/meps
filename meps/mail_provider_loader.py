import importlib

from mail_providers.mailgun_provider import MailgunProvider


class Error(Exception):
    pass


class MissingApiKeyError(Error):
    pass


class UnsupportedMailProviderError(Error):
    pass


class MailProviderLoader:

    def __init__(self, config):
        self.providers = []

        if 'mailgun_provider_api_key' not in config:
            raise MissingApiKeyError

        default_mail_provider = config.get(
            'default_mail_provider', 'MailgunProvider')

        if default_mail_provider == 'MailgunProvider':
            self.providers.append(MailgunProvider(
                config['mailgun_provider_api_key']))
        else:
            raise UnsupportedMailProviderError

    def get_providers(self):
        return self.providers
