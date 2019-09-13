from email.mime.text import MIMEText

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
        SMTP.sender = login_parameters["username"]
        SMTP.initialized = True
    
    @staticmethod
    async def send_message(*args, **kwargs):
        client = aiosmtplib.SMTP(**SMTP.client_parameters)
        await client.connect()
        await client.login(**SMTP.login_parameters)
        await client.send_message(*args, **kwargs)
        await client.quit()

    @staticmethod
    async def send_verify_mail(reciever, activation_code):
        content = (
            "請點擊下方連結驗證您的帳號：\n"
            "https://yunnet.yuntech.edu.tw/#/register_verify/{0}\n"
            "\n"
            "Please click following link to activate your account:\n"
            "https://yunnet.yuntech.edu.tw/#/register_verify/{0}\n"
            "\n"
            "連結有效時間為一小時."
            "Verify link will expire in 1 hour.\n"
            "\n"
            "如果連結過期,請重新註冊"
            "If link expired, Please register again."
        )
        mail = MIMEText(content.format(activation_code), _charset="big5")
        mail["Subject"] = "YunNet account Verify"
        mail["From"] = SMTP.sender
        mail["To"] = reciever
        await SMTP.send_message(mail)

    @staticmethod
    async def send_recovery_mail(reciever, recovery_code):
        content = (
            "請點擊下方連結重置您的密碼：\n"
            "https://yunnet.yuntech.edu.tw/#/set_password/{0}\n"
            "\n"
            "\n"
            "Please click following link to reset your password:\n"
            "https://yunnet.yuntech.edu.tw/#/set_password/{0}\n"
            "\n"
            "\n"
            "連結有效時間為一小時."
            "Verify link will expire in 1 hour. \n"
            "\n"
            "如果連結過期,請重新申請."
            "If link expire, Please re-apply"
            "\n"
        )
        mail = MIMEText(content.format(recovery_code), _charset="big5")
        mail["From"] = SMTP.sender
        mail["To"] = reciever
        mail["Subject"] = "YunNet Password Reset"
        await SMTP.send_message(mail)
        