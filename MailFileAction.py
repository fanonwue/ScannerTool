from FileAction import FileAction
from SmtpConfig import SmtpConfig
from EmailConfig import EmailConfig
from pathlib import Path
from smtplib import SMTP
from email import policy, utils, message
import ssl


class MailFileAction(FileAction):

    def __init__(self, target_mail: str, smtp_config: SmtpConfig, email_config: EmailConfig):
        self.target_mail = target_mail
        self.__smtp_config = smtp_config
        self.__email_config = email_config

    def execute(self, file: Path):
        """Execute an action on the given file path"""
        # alias the config objects to make access easier
        smtp_conf = self.__smtp_config
        mail_conf = self.__email_config

        msg = message.EmailMessage(policy.SMTPUTF8)
        # create Message-ID using python-provided utility functions
        msg['Message-ID'] = mail_conf.get_messge_id()
        msg['Subject'] = mail_conf.subject
        msg['From'] = smtp_conf.mail_from
        msg['To'] = self.target_mail
        msg.set_content(mail_conf.body)

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
            server = SMTP(smtp_conf.host, smtp_conf.port)
            server.starttls(context=context)
            server.login(smtp_conf.username, smtp_conf.password)
            server.send_message(msg)
        except Exception as e:
            print(e)
        finally:
            if server:
                server.quit()
