from email.utils import make_msgid


class EmailConfig:
    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body


    @staticmethod
    def get_default():
        # TODO make a config file instead of hardcoding
        config = {
            "subject": "Your scanned document",
            "body": "The scanned document is attached to this message",
        }
        return EmailConfig(**config)

    def get_messge_id(self):
        return make_msgid("scannertool")
