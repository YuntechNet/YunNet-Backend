from sanic import Sanic
from aiohttp import ClientSession, ClientResponse


RECAPTCHA_ENDPOINT = "https://www.google.com/recaptcha/api/siteverify"


async def verify_recaptcha(
    aiohttp_session: ClientSession, secret, g_recaptcha_response
) -> bool:
    """
    Verify reCaptcha response

    Attributes:
        aiohttp_session -- Initialized aiohttp ClientSession
        secret -- reCaptcha secret key
        g_recaptcha_response -- User responded token
        
    Returns:
        bool -- True if reCaptcha verification is success
    """
    recaptcha_data = {"secret": secret, "response": g_recaptcha_response}
    async with aiohttp_session.post(
        RECAPTCHA_ENDPOINT, data=recaptcha_data
    ) as response:
        response: ClientResponse = response
        json_response = await response.json()
        if json_response["success"]:
            return True
        else:
            return False
