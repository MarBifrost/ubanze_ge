from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(email, subject, message):
    print(f"Task triggered: Sending email to {email}")
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='ubanze6@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
