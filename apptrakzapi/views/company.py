from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company


class CompanyView(ViewSet):
    """ Company ViewSet """

    def update(self, request, pk=None):
        """
        Handle PUT requests for a company
        """
        company = Company.objects.get(pk=pk)
        company.name = request.data["name"]
        company.address1 = request.data["address1"]

        if "address2" in request.data:
            company.address2 = request.data["address2"]

        company.city = request.data["city"]
        company.state = request.data["state"]
        company.zipcode = request.data["zipcode"]
        company.website = request.data["website"]

        # Validate company data then serialize
        try:
            company.clean_fields()
            company.save()
            serializer = CompanySerializer(company, context={'request': None})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response(ex.args[0], status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """ Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        company = Company()
        company.user = current_user
        company.name = request.data["name"]
        company.address1 = request.data["address1"]

        if "address2" in request.data:
            company.address2 = request.data["address2"]

        company.city = request.data["city"]
        company.state = request.data["state"]
        company.zipcode = request.data["zipcode"]
        company.website = request.data["website"]

        # Validate company data then serialize
        try:
            company.clean_fields()
            company.save()
            serializer = CompanySerializer(company, context={'request': None})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response(ex.args[0], status=status.HTTP_400_BAD_REQUEST)

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
