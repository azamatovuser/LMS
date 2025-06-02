from apps.account.serializers import AccountRegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.account.models import Account

class AccountRegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AccountRegisterSerializer