from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


# We based it on the generic viewset and mixins
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # we modify the viewset to filter objects for the auth user
    # it overrides the method get_queryset
    # we add the custom filter of the queryset
    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
