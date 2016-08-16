# Multiple Email Providers Service (MEPS)

The MEPS project is designed to easily and reliably send email.

The current default provider is Mailgun. The default provider can be changed in
`meps_config.json`. The value passed to the "default_mail_provider" parameter is
the mail provider's class name. The following is an example:


```
{
    "default_mail_provider": "MailgunProvider",
    "mailgun_provider_api_key": "my_key"
}

```

The `default_mail_provider` parameter is optional. The
`mailgun_provider_api_key` is required, as the Mailgun provider requires an API
key.

## Install Instructions

Install the app from the root of the MEPS repo:

`pip install --editable .`

## Run Instructions

To run MEPS, change directory to the MEPS repo root and enter the following in
your terminal:

```
export FLASK_APP=meps.meps
flask run
```

The app launches on `http://localhost:5000/` by default.

Currently, only email sent via POST requests are accepted. The default endpoint
for sending mail via POST requests is:

```
http://localhost:5000/email
```

## Test Instructions

Tests rely on `pytest`. Tests can be run from the root directory with the
following:

```
python setup.py test
```

## Design

MEPS uses Python and Flask, a microframework, to send mail through multiple
mail servers.

Python was chosen for its simplicity, plentiful libraries, and ease of use
around servers and testing.

Flask was chosen for its simplicity, clear documentation, and ease of use. Flask
also makes it very easy to deal with application context and request context,
ensuring that each request is independent and can easily be handled in a RESTful
manner.

However, Flask, being based on WSGI, is fundamentally synchronous and blocking.
If MEPS begins to require higher performance under heavier request loads, then
an asynchronous framework like Twisted Klein would be more suitable.

MEPS has its core Flask server located in `meps/meps.py`. The server config is
located at `meps/meps_config.json` and allows the specification of the default
mail provider and the API key for Mailgun.

### Email Request Validation

Each email sent to the email endpoint is validated by the `request_validator`
module before being sent to the mail providers. The emails must meet the
following requirements:

1) The fields 'to', 'to_name', 'from', 'from_name', 'subject', and
   'body' exist in the mail request
2) Both 'to' and 'from' contain valid email addresses.

### Mail Provider Loader

MEPS loads mail providers based on the `meps_config.json` through the
`MailProviderLoader` class. `MailProviderLoader` loads all supported mail
providers.

MEPS then iterates through each mail provider and sends mail until one mail
provider succeeds, or all mail providers fail.

### Mail Providers

Each mail provider is intended to be very simple and self-contained. The
`MailgunProvider` class sends the given email to the Mailgun service via a
single POST request to the Mailgun HTTP API.

Mailgun is currently the only supported mail provider.

### Tests

Each component is unit-tested. All tests are located under the `meps/tests/`
directory and use `pytest`. See the Test Instructions for running tests.

## Future Goals

### Database

Adding a database to store mail data would be useful for long-term querying. It
may be helpful to store the mail locally for later retrieval and analysis.

Privacy is a concern, however, as some users may send personal information that
they do not intend for others to store and read.

### Frontend

No frontend currently exists for MEPS, as it was designed to be a simple HTTP
service. Adding a page for a user to send email would make the project more
user-friendly.

### Dynamic Configs

By changing the config file to specify the module, class name, and API key of
mail providers, it becomes possible to dynamically load mail providers as long
as they exist under `mail_providers/` and are specified in the config. The
default mail provider would be the first mail provider specified in the config,
or could be specified by a different config parameter.

It may be wiser to test with multiple mail providers before implementing the
above feature, as some mail providers may require much different configuration
than a simple API key.