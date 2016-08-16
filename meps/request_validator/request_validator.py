# -*- coding: utf-8 -*-
"""
    Request Validator
    ----------

    Validates the format of email requests.
"""
from validate_email import validate_email


def validate_email_request(email):
    """Validates email requests

    Args:
        email: Dictionary containing the email request.

    Returns:
        True if and only if the following conditions are met:

        1) The fields 'to', 'to_name', 'from', 'from_name', 'subject', and
            'body' exist in the email request
        2) Both 'to' and 'from' contain valid email addresses.

        If either condition is not met, then returns False.
    """
    if 'to_name' not in email or 'from_name' not in email:
        return False

    if 'to' not in email or not validate_email(email['to']):
        return False

    if 'from' not in email or not validate_email(email['from']):
        return False

    if 'subject' not in email or 'body' not in email:
        return False

    return True
