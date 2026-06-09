import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import Config

logger = logging.getLogger(__name__)

class EmailNotifier:
    @staticmethod
    def send_trade_notification(subject, body, attachment_path=None):
        if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
            logger.warning("SMTP credentials not set. Skipping email notification.")
            return

        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_USER
        msg['To'] = Config.EMAIL_RECIPIENT
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {attachment_path}",
                    )
                    msg.attach(part)
            except Exception as e:
                logger.error(f"Failed to attach file {attachment_path}: {e}")

        try:
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            logger.info(f"Notification email sent to {Config.EMAIL_RECIPIENT}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
