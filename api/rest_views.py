from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .serializers import *
import json
from django.contrib.auth.models import User
from wordpress.models import WpUsers
# from django.conf import settings

class RegisterFromServerView(APIView):
    """
    view to register user in current as well as other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # serializer =  RegistrationSerializer(data=request.data)
        data = request.data
        username = data['username']
        user_email = data['email']
        if not (WpUsers.objects.filter(user_login=username).exists() or WpUsers.objects.filter(user_email = user_email).exists()):
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email = user_email).exists()):
                password = data['password']
                #No confirm password is being provied, so not password checks
                user_nicename = data['user_nicename']
                user_url = data.get('user_url', None)
                display_name = data.get('display_name', None)
                user = User.objects.create_user(username = username, email = user_email, password = password)
                wp_user = WpUsers()
                wp_user.user_login = username
                wp_user.user_pass = user.password[7:]
                wp_user.user_nicename = user_nicename
                wp_user.user_email = user_email
                # wp_user.user_url = user_url
                wp_user.display_name = display_name
                wp_user.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK, content_type='application/json')
        return Response(data={'status': False}, status=status.HTTP_400_BAD_REQUEST)

class UpdateFromServerView(APIView):
    """
    View update the user profile from other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        if User.objects.filter(username=username).exists() and WpUsers.objects.filter(user_login=username).exists():
            user = User.objects.get(username=username)
            wp_user = WpUsers.objects.get(user_login=user.username)
            user_email = data.get("user_email", wp_user.user_email)
            wp_user.user_email = user_email
            user.email = user_email
            wp_user.user_nicename = data.get('user_nicename', wp_user.user_nicename)
            wp_user.display_name = data.get('display_name', wp_user.display_name)
            wp_user.user_url = data.get('user_url', wp_user.user_url)
            user.save()
            wp_user.save()
            return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordFromServerView(APIView):
    """
    View to change the user password from other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data['username']
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={'status': False}, status=status.HTTP_404_NOT_FOUND)

        try:
            wp_user = WpUsers.objects.get(user_login=user.username)
        except WpUsers.DoesNotExist:
            return Response(data={'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not (new_password == old_password):
            DatabasePassword = user.password
            from django.contrib.auth.hashers import check_password
            chk = check_password(password=old_password, encoded = DatabasePassword)
            if chk == True:
                user.set_password(new_password)
                user.save()
                wp_user = WpUsers.objects.get(user_login=user.username)
                wp_user.user_pass = user.password[7:]
                wp_user.save()
                return Response(data={'status': True}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'status': False}, status=status.HTTP_304_NOT_MODIFIED)

class UpdateUserInfoView(APIView):
    """
    View to update user info from other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        update = data['update']
        username = data['username']
        if User.objects.filter(username=username).exists() and WpUsers.objects.filter(user_login=username).exists():
            user = User.objects.get(username=username)
            wp_user = WpUsers.objects.get(user_login=user.username)
            if "name" in update:
                wp_user.user_nicename = update['name']
                wp_user.display_name = update['name']
                wp_user.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK)
            # user_email = data.get("user_email", wp_user.user_email)
            # wp_user.user_email = user_email
            # user.email = user_email
            # wp_user.user_url = data.get('user_url', wp_user.user_url)
            # user.save()
            # wp_user.save()
        return Response(data={'status': False}, status=status.HTTP_400_BAD_REQUEST)

class ChangeEmailView(APIView):
    """
    View to change the user email from other server
    """
    # authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        new_user_email = data['email']
        if User.objects.filter(username=username).exists() and WpUsers.objects.filter(user_login=username).exists():
            user = User.objects.get(username=username)
            wp_user = WpUsers.objects.get(user_login=user.username)
            wp_user.user_email = new_user_email
            user.email == new_user_email
            user.save()
            wp_user.save()
            return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_400_BAD_REQUEST)

# class ChangeUsernameFromServerView(APIView):
#     """
#     View to change the username from other server
#     """
#     authentication_classes = (TokenAuthentication,)
#     renderer_classes = (JSONRenderer,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         user = User.objects.get(username=request.user.username)
#         old_username = user.username
#         new_username = request.data['new_username']
#         if new_username == old_username:
#             return Response(data={'status': False}, status=status.HTTP_304_NOT_MODIFIED)
#         else:
#             user.username = new_username
#             wp_user = WpUsers.objects.get(user_login=old_username)
#             wp_user.user_login = new_username
#             user.save()
#             wp_user.save()
#             return Response(data={'status': True}, status=status.HTTP_200_OK)
