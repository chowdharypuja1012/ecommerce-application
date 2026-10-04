from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Address, Profile
from .serializers import (
    AddressSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """
    POST /api/v1/auth/register/
    Public endpoint for registering a new user.
    Generates DRF auth token upon creation.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User registered successfully.",
                    "token": token.key,
                    "user": UserSerializer(user).data,
                    "profile": ProfileSerializer(user.profile).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Public endpoint for authenticating user credentials.
    Returns auth token on success.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Login successful.",
                    "token": token.key,
                    "user": UserSerializer(user).data,
                    "profile": ProfileSerializer(user.profile).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Authenticated endpoint to invalidate/delete the user's auth token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    GET /api/v1/auth/me/
    Authenticated endpoint to retrieve the current user's info and profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user": UserSerializer(request.user).data,
                "profile": ProfileSerializer(request.user.profile).data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    """
    GET /api/v1/profile/
    PUT /api/v1/profile/
    PATCH /api/v1/profile/
    Authenticated endpoint for viewing and updating user's own profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        return self._update_profile(request, partial=False)

    def patch(self, request):
        return self._update_profile(request, partial=True)

    def _update_profile(self, request, partial=False):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()

            # Optional update first_name / last_name if supplied in user object
            user_data = request.data.get("user", {})
            if isinstance(user_data, dict):
                if "first_name" in user_data:
                    request.user.first_name = user_data["first_name"]
                if "last_name" in user_data:
                    request.user.last_name = user_data["last_name"]
                request.user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressListCreateView(ListCreateAPIView):
    """
    GET /api/v1/profile/addresses/
    POST /api/v1/profile/addresses/
    Authenticated endpoint for listing and creating addresses strictly owned by request.user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/profile/addresses/<id>/
    PUT /api/v1/profile/addresses/<id>/
    DELETE /api/v1/profile/addresses/<id>/
    Authenticated endpoint for managing a single address.
    Strictly enforces user ownership (403 Forbidden if address belongs to another user).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
