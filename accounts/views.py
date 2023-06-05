from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer,ProfileSerializers,ChangePasswordSerializer,ChangeUsernameSerializers
from rest_framework import status
from .models import Profile
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions,generics
from .permission import IsObjectOwner


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        profile, created_profile = Profile.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'profile_id': profile.pk,
        })

@api_view(['POST', ])
def registration_views(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        dataa = {}

        if serializer.is_valid():
            user = serializer.save()

            dataa['response'] = 'Registration Successfully'
            dataa['username'] = user.username
            dataa['email'] = user.email

        else:
            dataa = serializer.errors

        return Response(dataa, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameView(generics.UpdateAPIView):
    serializer_class = ChangeUsernameSerializers
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.username = serializer.data.get("new_username")
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'username updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializers(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,IsObjectOwner,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializers(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializers(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)