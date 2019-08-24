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
        client_parameters = client_parameters
        login_parameters = login_parameters
        SMTP.sender = login_parameters["username"]
        SMTP.initialized = True
    
    @staticmethod
    async def send_message(*args, **kwargs):
        client = aiosmtplib.SMTP(**SMTP.client_parameters)
        await client.connect()
        await client.login(**SMTP.login_parameters)
        await client.send_message(*args, **kwargs)
        await client.quit()
