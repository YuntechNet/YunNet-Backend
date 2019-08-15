import aiosmtplib


class SMTP:
    """
    SMTP namespace
    """

    client: aiosmtplib.SMTP = None
    sender: str = None


    @staticmethod
    async def init(client_parameters, login_parameters):
        if SMTP.client is None:
            SMTP.client = aiosmtplib.SMTP(**client_parameters)
            await SMTP.client.connect()
            await SMTP.client.login(**login_parameters)
            SMTP.sender = login_parameters["username"]
        return SMTP
