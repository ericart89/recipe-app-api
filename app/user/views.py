from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # the renderer class sets the renderer so we can view
    # this endpoint in the browser
    # in this way you can login with chrome and type everything
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # mechanism used for authentication
    authentication_classes = (authentication.TokenAuthentication,)
    # level of access that the user has
    # we dont want to give any permissions, just log in
    permission_classes = (permissions.IsAuthenticated,)

    # we need to add a get function to the view
    # we will use the model for the logged in user (override)
    def get_object(self):
        """Retrieve and return authentication user"""
        # the authentication classes take care of getting the
        # auth user and assign it to the request (django)
        return self.request.user
