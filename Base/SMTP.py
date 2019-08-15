import aiosmtplib


class SMTP:
    client: aiosmtplib.SMTP = None

    """
    SMTP namespace
    """

    @staticmethod
    async def init(client_parameters, login_parameters):
        if SMTP.client is None:
            SMTP.client = aiosmtplib.SMTP(**client_parameters)
            await SMTP.client.connect()
            await SMTP.client.login(**login_parameters)
        return SMTP
