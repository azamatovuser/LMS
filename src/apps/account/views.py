from apps.account.serializers import UserRegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.account.models import User

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer