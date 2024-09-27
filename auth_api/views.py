from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .emails import send_verification_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken, TokenError

class RegisterApi(APIView):
    def post(self, request):
        try:
            data = request.data
            print("data is:",data)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                print(user)
                print(user.email)
                send_verification_email(user.email)
                return Response({
                    'status': 200,
                    'message': "Registration successfully. Check email.",
                    'data': serializer.data,
                }, status=status.HTTP_201_CREATED) 
            return Response({
                'status': 400,
                'message': "Invalid data. Please try again.",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': "Internal Server Error.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class VerifyOtp(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             serializer = VerifyAccountSerialization(data=data)
#             if serializer.is_valid():
#                 email = serializer.data['email']
#                 otp = serializer.data['otp']
#                 user = User.objects.filter(email=email)
#                 if not user.exists():
#                     return Response({
#                         'status': 400,
#                         'message': "Invalid Email",
#                         'errors': 'invalid Email'
#                     })

#                 if user[0].otp != otp:
#                     return Response({
#                         'status': 400,
#                         'message': "Wrong OTP",
#                         'data': "Wrong OTP"
#                     })

#                 user = user.first()
#                 user.is_verified = True
#                 user.save()

#                 return Response({
#                     'status': 200,
#                     'message': "Account Verified",
#                 })

#             return Response({
#                 'status': 400,
#                 'message': "Invalid Data",
#                 'errors': serializer.errors
#             }, status=400)  # Set status code explicitly to 400 for invalid data

#         except Exception as e:
#             print(e)
#             return Response({
#                 'status': 500,
#                 'message': "Internal Server Error",
#             }, status=500) 


class VerifyAccount(APIView):
    def get(self, request):
        token = request.query_params.get('token')  
        try:
            # Validate the token
            UntypedToken(token)  # This will raise an error if the token is invalid
            return Response({
                'status': 200,
                'message': 'Token is valid.'
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                'status': 400,
                'message': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error.',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

