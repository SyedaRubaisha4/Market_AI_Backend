import os
from datetime import datetime, timezone
import os
from datetime import datetime, timezone
from django.conf import settings

STORAGE_DIR = str(settings.MEDIA_ROOT)
STORAGE_PATH = settings.MEDIA_URL.strip('/')
SETTING_CONTENT_DIR = settings.SETTING_CONTENT_DIR

SMTP_SENDER_EMAIL = settings.SMTP_SENDER_EMAIL
SMTP_PASSWORD = settings.SMTP_PASSWORD
SMTP_PORT = settings.SMTP_PORT
SMTP_HOSTNAME = settings.SMTP_HOSTNAME
SMTP_USE_SECURE = settings.SMTP_USE_SECURE
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import uuid

class HelperFunctions():
    @staticmethod
    def save_file(image, file_name, file_path, ext=''):
        upload_to = os.path.join(STORAGE_DIR, file_path)
        os.makedirs(upload_to, exist_ok=True)
        file_name = file_name if file_name != None else HelperFunctions.generate_timestamp_string()
        file_name = file_name + os.path.splitext(image.name)[1]
        upload_to = os.path.join(upload_to, file_name)
        with open(upload_to, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        return os.path.join(STORAGE_PATH, file_path, file_name)
    @staticmethod
    def unique_filename(original_name):
        ext = os.path.splitext(original_name)[1]  
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return unique_name
    @staticmethod
    def generate_timestamp_string():
        # Get the current date and time
        current_time = HelperFunctions.get_current_datetime()
        # Format the date and time into the desired string format
        timestamp_string = current_time.strftime('%Y%m%d%H%M%S%f')
        return timestamp_string

    @staticmethod
    def extension(filename):
        filename, file_extension = os.path.splitext(filename)
        return file_extension

    @staticmethod
    def generate_random_code():
        # return '0000'
        return '{:04}'.format(random.randint(0, 9999))

    @staticmethod
    def get_current_datetime():
        return datetime.now(timezone.utc)

    @staticmethod
    def save_text_to_file(text, filename, file_path):
        full_path = os.path.join(STORAGE_DIR, file_path)
        os.makedirs(full_path, exist_ok=True)
        full_path = os.path.join(full_path, filename)
        with open(full_path, "a") as file:
            file.write(text + "\n")

    @staticmethod
    def read_html_as_string(file_path, filename):
        html_path = os.path.join(SETTING_CONTENT_DIR, file_path, filename)

        with open(html_path, 'r', encoding='utf-8-sig') as f:
            html_string = f.read()
        html_string = html_string.replace('\r\n', '')
        html_string = html_string.replace('\n', '')
        return html_string

    @staticmethod
    def send_email(receiver_email, subject, html_content):

        # Email configuration
        smtp_user = SMTP_SENDER_EMAIL
        password = SMTP_PASSWORD
        smtp_server = SMTP_HOSTNAME
        smtp_port = SMTP_PORT
        sender_email = smtp_user

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(html_content, "html"))

        try:
            # Create a secure SSL context
            server = smtplib.SMTP(smtp_server, smtp_port)
            if (SMTP_USE_SECURE):
                server.starttls()  # Secure the connection
            server.login(smtp_user, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            server.quit()

    @staticmethod
    def generate_referral_code(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        referral_code = ''.join(random.choice(letters_and_digits) for i in range(length))
        return referral_code
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string


class HelperFunctions():
    @staticmethod
    def unique_filename(original_name):
        ext = os.path.splitext(original_name)[1]  
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return unique_name
    
    @staticmethod
    def save_file(image, file_name, file_path):
        upload_to = os.path.join(STORAGE_DIR, file_path)
        os.makedirs(upload_to, exist_ok=True)

        ext = os.path.splitext(image.name)[1]
        file_name = file_name + ext
        final_path = os.path.join(upload_to, file_name)

        with open(final_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        return os.path.join(STORAGE_PATH, file_path, file_name)


    @staticmethod
    def generate_timestamp_string():
        # Get the current date and time
        current_time = HelperFunctions.get_current_datetime()
        # Format the date and time into the desired string format
        timestamp_string = current_time.strftime('%Y%m%d%H%M%S%f')
        return timestamp_string

    @staticmethod
    def extension(filename):
        filename, file_extension = os.path.splitext(filename)
        return file_extension

    @staticmethod
    def generate_random_code():
        # return '0000'
        return '{:04}'.format(random.randint(0, 9999))

    @staticmethod
    def get_current_datetime():
        return datetime.now(timezone.utc)

    @staticmethod
    def save_text_to_file(text, filename, file_path):
        full_path = os.path.join(STORAGE_DIR, file_path)
        os.makedirs(full_path, exist_ok=True)
        full_path = os.path.join(full_path, filename)
        with open(full_path, "a") as file:
            file.write(text + "\n")

    @staticmethod
    def read_html_as_string(file_path, filename):
        html_path = os.path.join(SETTING_CONTENT_DIR, file_path, filename)

        with open(html_path, 'r', encoding='utf-8-sig') as f:
            html_string = f.read()
        html_string = html_string.replace('\r\n', '')
        html_string = html_string.replace('\n', '')
        return html_string

    @staticmethod
    def send_email(receiver_email, subject, html_content):

        # Email configuration
        smtp_user = SMTP_SENDER_EMAIL
        password = SMTP_PASSWORD
        smtp_server = SMTP_HOSTNAME
        smtp_port = SMTP_PORT
        sender_email = smtp_user

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(html_content, "html"))

        try:
            # Create a secure SSL context
            server = smtplib.SMTP(smtp_server, smtp_port)
            if (SMTP_USE_SECURE):
                server.starttls()  # Secure the connection
            server.login(smtp_user, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            server.quit()

    @staticmethod
    def generate_referral_code(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        referral_code = ''.join(random.choice(letters_and_digits) for i in range(length))
        return referral_code