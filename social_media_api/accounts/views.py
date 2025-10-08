from rest_framework import generics, status
from rest_framework.response import Response
from accounts.serializers import RegisterSerializer, ProfileSerializer
from rest_framework.authtoken.models import Token


# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": RegisterSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
