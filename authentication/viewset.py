from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import SignupSerializer, LoginSerializer, EmptySerializer


class AuthenticationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmptySerializer

    def get_serializer_class(self):
        if self.action == 'signup':
            return SignupSerializer
        if self.action == 'login':
            return LoginSerializer
        else:
            return EmptySerializer


    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
