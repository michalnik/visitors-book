from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from account.serializers import UserSerializer


# Create your views here.
class RegisterView(CreateAPIView):
    """Enable register user with username, email and password
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
