# -*- coding: utf-8 -*-
"""
    Request Validator
    ----------

    Validates the format of mail requests.
"""
from validate_email import validate_email


def validate_mail_request(mail):
    """Validates mail requests

    Args:
        mail: Dictionary containing the mail request.

    Returns:
        True if and only if the following conditions are met:

        1) The fields 'to', 'to_name', 'from', 'from_name', 'subject', and
            'body' exist in the mail request
        2) Both 'to' and 'from' contain valid email addresses.

        If either condition is not met, then returns False.
    """
    if 'to_name' not in mail or 'from_name' not in mail:
        return False

    if 'to' not in mail or not validate_email(mail['to']):
        return False

    if 'from' not in mail or not validate_email(mail['from']):
        return False

    if 'subject' not in mail or 'body' not in mail:
        return False

    return True
