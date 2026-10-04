from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Address, Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Public details serializer for User."""
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "full_name", "phone_number", "avatar_url", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address CRUD."""
    class Meta:
        model = Address
        fields = (
            "id",
            "title",
            "street_address",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration with framework password validation."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    phone_number = serializers.CharField(max_length=50, required=False, allow_blank=True, default="")

    def validate_username(self, value):
        username = value.strip()
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        full_name = validated_data.get("full_name", "")
        phone_number = validated_data.get("phone_number", "")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Update profile created via signal
        if hasattr(user, "profile"):
            profile = user.profile
            if full_name:
                profile.full_name = full_name
            if phone_number:
                profile.phone_number = phone_number
            profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for authenticating login credentials."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        # Try username or email authentication
        user = authenticate(username=username, password=password)
        if not user:
            # Check if username is an email address
            user_by_email = User.objects.filter(email__iexact=username).first()
            if user_by_email:
                user = authenticate(username=user_by_email.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials provided.")
        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        data["user"] = user
        return data
