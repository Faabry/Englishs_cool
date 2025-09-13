import random
from django.core.mail import send_mail

def send_verification_email(user):
    code = str(random.randint(100000, 999999))  # 6-digit code
    user.profile.verification_code = code
    user.profile.save()
    send_mail(
        "Verify your email",
        f"Your verification code is {code}",
        "noreply@yourapp.com",  # change this to your email
        [user.email],
        fail_silently=False,
    )
