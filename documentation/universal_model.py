from sanic_openapi import doc


class Message:
    message = doc.String("Message")