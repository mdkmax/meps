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
