from django.contrib.auth.models import User
from django.http import HttpResponseServerError
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
            companies, many=True, context={'request': None})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            company = Company.objects.get(pk=pk, user=current_user)

            serializer = CompanySerializer(
                company, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'url', 'name', 'address1', 'address2',
                  'city', 'state', 'zipcode', 'website')
        depth = 1
