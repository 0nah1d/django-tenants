from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'address']


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userprofile']

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile', None)

        # Update user instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create user profile
        if userprofile_data:
            UserProfile.objects.update_or_create(user=instance, defaults=userprofile_data)

        return instance
