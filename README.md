# Multiple Email Providers Service (MEPS)

The MEPS project is designed to easily and reliably send email.

Given a list of email providers and a small provider-specific implementation,
the user can send email through a list of providers. MEPS will try each provider
one at a time until one provider succeeds, or they all fail to send.
