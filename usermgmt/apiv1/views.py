from rest_framework.generics import CreateAPIView
from ..models import User
from .serializers import UserCreateSerializer

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()