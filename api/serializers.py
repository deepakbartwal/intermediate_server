from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.Serializer):
    """Form for user registration/creating account"""
    user_email = serializers.EmailField()
    username = serializers.CharField(max_length=60)
    user_nicename = serializers.CharField(max_length = 50)
    user_url = serializers.URLField(max_length=100)
    display_name = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length = 30)
    confirm_password = serializers.CharField(max_length=30)

    def test(self):
        return True

class UpdateProfileSerializer(serializers.Serializer):
    """ Serializers for updating user information """
    user_email = serializers.EmailField()
    user_nicename = serializers.CharField(max_length = 50)
    user_url = serializers.URLField(max_length=100)
    display_name = serializers.CharField(max_length=250)


#     def update(self, user_instance, validated_data):
#         user_instance.email = validated_data.get('user_email', user_instance.email)
#         user_instance.save()
#         up_instance = UserProfile.object.get(user = user_instance)
#         up_instance.user_nicename = validated_data.get('user_nicename', up_instance.user_nicename)
#         up_instance.user_url = validated_data.get('user_url', up_instance.user_url)
#         up_instance.display_name = validated_data.get('display_name', up_instance.display_name)
#         up_instance.save()
#         return user_instance
