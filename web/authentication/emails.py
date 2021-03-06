import os
import sendgrid

from sendgrid import SendGridClientError, SendGridServerError


class SendGrid(object):
    """
    This class is used to send emails using the requests
    module to the sendgrid message api.
    Attributes:
        sg: An instance of the SendGrid Client.
    """

    sg = sendgrid.SendGridClient(os.getenv('sendgrid_apikey'),
                                 raise_errors=True)

    @staticmethod
    def compose(sender, recipient, subject, text="", html="None"):
        """
        RECOMMENDED: use this method to compose the email.
        Returns: A mail instance.
        """
        message = sendgrid.Mail()
        message.add_to(recipient)
        message.set_subject(subject)
        message.set_html(html)
        message.set_text(text)
        message.set_from(sender)

        return message

    @staticmethod
    def send(message):
        """Sends a message using SendGrid's messaging API.
        Returns: A status code.
        Raises:
            SendGridClientError,
            SendGridServerError
        """
        try:
            http_status_code, message = SendGrid.sg.send(message)
        except SendGridClientError:
            pass
        except SendGridServerError:
            pass

        return http_status_code
