from validate_email import validate_email


def validate_mail_request(mail):
    if 'to_name' not in mail or 'from_name' not in mail:
        return False

    if 'to' not in mail or not validate_email(mail['to']):
        return False

    if 'from' not in mail or not validate_email(mail['from']):
        return False

    if 'subject' not in mail or 'body' not in mail:
        return False

    return True
