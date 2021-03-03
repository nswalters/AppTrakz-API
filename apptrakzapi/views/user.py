from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Profile, SocialMedia, SocialMediaType


class UserProfileSocialTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for a usre social media type
    """
    class Meta:
        model = SocialMediaType
        fields = ('name',)


class UserProfileSocialSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for user social media records in a profile
    """
    type = UserProfileSocialTypeSerializer(many=False)

    class Meta:
        model = SocialMedia
        fields = ('name', 'url', 'type')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for a user record in a profile
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'last_login', 'date_joined')
        depth = 1


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    JSON serializer for profile
    """

    user = UserProfileSerializer(many=False)
    social_media = UserProfileSocialSerializer(many=True)

    class Meta:
        model = Profile
        url = serializers.HyperlinkedIdentityField(
            view_name='profile',
            lookup_field='id'
        )
        fields = ('id', 'bio', 'profile_image', 'user', 'social_media')
        depth = 1


class UserView(ViewSet):
    @action(methods=['GET', 'PUT'], detail=False)
    def profile(self, request):

        if request.method == 'PUT':
            user_profile = Profile.objects.get(user=request.auth.user)
            if 'bio' in request.data:
                user_profile.bio = request.data['bio']
            else:
                user_profile.bio = None

            if 'profile_image' in request.data:
                user_profile.profile_image = request.data['profile_image']
            else:
                user_profile.profile_image = None

            user_profile.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        if request.method == 'GET':
            try:
                profile = Profile.objects.get(user=request.auth.user)

                profile.social_media = SocialMedia.objects.filter(
                    profile=profile)

                serializer = ProfileSerializer(
                    profile, many=False, context={'request': request})

                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)
