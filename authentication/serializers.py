from django.contrib.auth.models import User
from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    pass


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        username, email, password, password2 = (
            attrs.get('username'),
            attrs.get('email'),
            attrs.get('password'),
            attrs.get('password2')
        )

        if password != password2:
            raise serializers.ValidationError({'password2': 'Passwords must match'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already registered'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        user = User.objects.filter(email=username_or_email).first()
        if not user:
            user = User.objects.filter(username=username_or_email).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid username/email or password')

        attrs['user'] = user
        return attrs


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ['email']


class ModifiedJWTSerializer(serializers.Serializer):
    access = serializers.CharField(source='access_token')
    refresh = serializers.CharField(source='refresh_token')
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return ProfileInfoSerializer(obj['user'], context=self.context).data
