# import random
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import User

# def send_otp_email(email):
#     try:
#         subject = 'Your Account verification email'
#         otp = random.randint(1000, 9999)
#         message = f'Your OTP is {otp}. Please use this OTP to verify your account.'
#         email_from = "rohankhan5990@gmail.com"
#         send_mail(subject, message, email_from, [email])
        
#         user_obj = User.objects.get(email=email)
#         user_obj.otp = otp
#         user_obj.save()                     
        
#         return True
#     except Exception as e:
#         print(f"Error sending OTP email to {email}: {e}")
#         return False  


import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

def send_verification_email(email):
    try:
        subject = 'Account Verification'
        user = User.objects.get(email=email)

        # Generate JWT token
        token = RefreshToken.for_user(user).access_token
        token['email'] = user.email  

        # Create a verification link
        verification_link = f"http://127.0.0.1:8000/verifyAccount/?token={token}"

        # Email message
        message = f'Click the link below to verify your account:\n{verification_link}'
        email_from = settings.DEFAULT_FROM_EMAIL  # Update as necessary
        send_mail(subject, message, email_from, [email])

        return True
    except Exception as e:
        print(f"Error sending verification email to {email}: {e}")
        return False
