import aiohttp


class aiohttpSession:
    """
    Create Pool object from parameters
    
    Args:
        tcp_connecter_args: dict
            Parameters for TCPConnector object
        client_session_args: dict
            Parameters for ClientSession object
            (connector key value will be ignored)
    """

    session: aiohttp.ClientSession = None

    @staticmethod
    async def init(
        tcp_connecter_args: dict = dict(), client_session_args: dict = dict()
    ):
        if aiohttpSession.session == None:
            connector = aiohttp.TCPConnector(**tcp_connecter_args)
            client_session_args["connector"] = connector
            aiohttpSession.session = aiohttp.ClientSession(**client_session_args)
        return aiohttpSession

    @staticmethod
    async def close():
        await aiohttpSession.session.close()
