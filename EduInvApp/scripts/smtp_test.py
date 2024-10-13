# smtp_test.py

from django.core.mail import send_mail
from django.conf import settings


def send_test_email():
    send_mail(
        'SMTP Test Email',
        'This is a test email sent from the Django application.',
        settings.EMAIL_HOST_USER,
        ['recipient-email@example.com'],  # Replace with a valid recipient email
        fail_silently=False,
    )

if __name__ == "__main__":
    send_test_email()
