from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from user.serializers import UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Ensure only the authenticated user's profile is accessible """
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        """ Retrieve only the authenticated user's profile """
        return self.request.user
