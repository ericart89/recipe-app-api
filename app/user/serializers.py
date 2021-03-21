from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self,attrs):
        """Validate and authenticate the user"""
        # attrs have the fields of the serializer
        # using get we can retrieve them
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # this is the way you access to the context of the request
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # if the previous command does not return a user (auth fails)
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code ='authentication')

        # we set the user
        attrs['user'] = user
        # if we override this function we return the attrs in the end
        return attrs


