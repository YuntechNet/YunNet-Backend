import aiosmtplib


class SMTP:
    """
    SMTP namespace
    """

    sender: str = None
    initialized = False
    client_parameters = {}
    login_parameters = {}

    @staticmethod
    async def init(client_parameters, login_parameters):
        SMTP.client_parameters = client_parameters
        SMTP.login_parameters = login_parameters
        SMTP.sender = "網管小組 <{0}>".format(login_parameters["username"])
        SMTP.initialized = True
    
    @staticmethod
    async def send_message(*args, **kwargs):
        client = aiosmtplib.SMTP(**SMTP.client_parameters)
        await client.connect()
        await client.login(**SMTP.login_parameters)
        await client.send_message(*args, **kwargs)
        await client.quit()
