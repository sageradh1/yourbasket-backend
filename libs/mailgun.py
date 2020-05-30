import os

from requests import post

FAILED_LOAD_API_KEY = "Failed to load MailGun API key"
FAILED_LOAD_DOMAIN = "Failed to load MailGun Domain"
ERROR_SENDING_EMAIL = "Error in sending confirmation email, user registration failed."


class MailGunException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Store REST API"
    FROM_EMAIL = "ashishsth1993@gmail.com"

    @classmethod
    def send_email(cls,  email, subject, text, html):
        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(FAILED_LOAD_DOMAIN)
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE}<{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html
            },
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)
        return response
