import smtplib

class SMTP:
    client: smtplib.SMTP = None

    '''
    
    '''
    @staticmethod
    async def init(client_parameters, login_parameters):
        if client is not None:
            client = smtplib.SMTP(**client_parameters)
            await client.connect()
            resp = await client.login(**login_parameters)
            if resp != 200:
                raise smtplib.SMTPAuthenticationError
        return SMTP
