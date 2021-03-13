from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company, Contact, Job, JobContact


class JobContactView(ViewSet):
    """ Job Contact ViewSet """

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for a specific job contact record
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            job_contact = JobContact.objects.get(pk=pk, job__user=current_user)

            serializer = JobContactSerializer(
                job_contact, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to list all job contacts for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        job_contacts = JobContact.objects.filter(job__user=current_user)

        serializer = JobContactSerializer(
            job_contacts, many=True, context={'request': None})

        return Response(serializer.data)


class ContactJobCompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'url', 'name')


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'phone', 'email')


class ContactJobSerializer(serializers.HyperlinkedModelSerializer):

    company = ContactJobCompanySerializer(many=False)

    class Meta:
        model = Job
        fields = ('id', 'url', 'role_title', 'company')
        depth = 1


class JobContactSerializer(serializers.HyperlinkedModelSerializer):

    contact = ContactSerializer(many=False)
    job = ContactJobSerializer(many=False)

    class Meta:
        model = JobContact
        fields = ('id', 'job', 'contact')
        depth = 1
