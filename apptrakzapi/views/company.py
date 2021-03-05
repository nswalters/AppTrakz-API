from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company


class CompanyView(ViewSet):

    def list(self, request):
        """
        Handle GET requests to list all companies for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Return companies sorted alphabetically
        companies = Company.objects.filter(user=current_user).order_by('name')

        serializer = CompanySerializer(
            companies, many=True, context={'request': request})

        return Response(serializer.data)


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'address1', 'address2',
                  'city', 'state', 'zipcode', 'website')
        depth = 1
