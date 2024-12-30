from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_client_email(subject, message, address):
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
        print(f"Email sent to {address}")
        return "Email sent successfully"  # Return a simple success message
    except Exception as e:
        print(f"Error sending email to {address}: {e}")
        return f"Error sending email: {e}"  # Return a simple error message
 