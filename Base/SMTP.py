import smtplib


class SMTP:
    client: smtplib.SMTP = None

    """
    
    """

    @staticmethod
    async def init(client_parameters, login_parameters):
        if SMTP.client is not None:
            SMTP.client = smtplib.SMTP(**client_parameters)
            await SMTP.client.connect()
            resp = await SMTP.client.login(**login_parameters)
            if resp != 200:
                raise smtplib.SMTPAuthenticationError
        return SMTP
