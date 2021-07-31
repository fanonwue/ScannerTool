from FileAction import FileAction
from SmtpConfig import SmtpConfig
from pathlib import Path
from smtplib import SMTP
from email import policy, utils, message
import ssl


class MailFileAction(FileAction):

    def __init__(self, mail: str):
        self.mail = mail
        self.__smtp_config = SmtpConfig.get_default()

    def execute(self, file: Path):
        """Execute an action on the given file path"""
        # alias the config object to make access easier
        config = self.__smtp_config

        msg = message.EmailMessage(policy.SMTPUTF8)
        # create Message-ID using python-provided utility functions
        msg['Message-ID'] = utils.make_msgid("scannertool")
        msg['Subject'] = "Gescanntes Dokument"
        msg['From'] = config.mail_from
        msg['To'] = self.mail
        msg.set_content("Im Anhang befindet sich das gescannte Dokument.")

        try:
            with open(file, 'rb') as file_obj:
                content = file_obj.read()
                # add the file content with the appropriate MIME-Type and filename to the message object
                msg.add_attachment(content, maintype="application", subtype="pdf", filename=file.name)

        except Exception as e:
            print(f"Error opening file at {file.absolute()}", e)
            # it's useless to send an email without any file attached, so just stop here
            return


        server = None

        try:
            # make sure to create the default security context according to
            # https://docs.python.org/3/library/ssl.html#ssl-security
            context = ssl.create_default_context()
            server = SMTP(config.host, config.port)
            server.starttls(context=context)
            server.login(config.username, config.password)
            server.send_message(msg)
        except Exception as e:
            print(e)
        finally:
            if server:
                server.quit()
