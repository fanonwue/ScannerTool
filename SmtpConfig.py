class SmtpConfig:
    def __init__(self, host: str, port: int, username: str, password: str, starttls: bool, mail_from: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.starttls = starttls

        if not mail_from:
            mail_from = self.username
        self.mail_from = mail_from


    @staticmethod
    def get_default():
        # TODO make a config file instead of hardcoding
        config = {
            "host": "mail.wuenderich.de",
            "port": 587,
            "username": "<redacted>",
            "password": "<redacted>",
            "starttls": True,
            "mail_from": None
        }
        return SmtpConfig(**config)