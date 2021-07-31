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
        """creates a default object for testing purposes"""
        config = {
            "host": "smtp.domain.com",
            "port": 587,
            "username": "user",
            "password": "password",
            "starttls": True,
            "mail_from": None
        }
        return SmtpConfig(**config)