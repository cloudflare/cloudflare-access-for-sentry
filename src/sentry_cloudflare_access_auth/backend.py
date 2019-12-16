from __future__ import absolute_import

# from django.conf import settings
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend

# class CloudflareAccessBackend(ModelBackend):
#     """
#     Authenticate using

#     Use the authentication information from the request to authenticate a user
#     by e-mail.
#     """

#     def authenticate(self, request, username=None, password=None):
#         login_valid = ("test" == username)
#         if login_valid:
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 # Create a new user. There's no need to set a password
#                 # because only the password from settings.py is checked.
#                 user = User(username=username)
#                 user.is_staff = True
#                 user.is_superuser = True
#                 user.save()
#             return user
#         return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None