from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
'''
We create a user activation email signal. When a new user register, we send a email.
'''

@receiver(post_save, sender = User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        # for a single user, we need to send a token for it's unique identification:
        token = default_token_generator.make_token(instance)
        # for every single user need a unique activation url:
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        subject = "Activate Your Account"
        message = f"Hi {instance.username},\n\nPlease activate your account by click the link:\n{activation_url}\n\nThank You!"
        recipient_list = [instance.email]
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list
            )
        except Exception as error:
            print(f"Failed to send email to {instance.email}: {str(error)}")