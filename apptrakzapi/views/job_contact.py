from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company, Contact, Job, JobContact


class JobContactView(ViewSet):
    """ Job Contact ViewSet """

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests for a job contact.

        The job contact record will be 'soft-deleted', i.e. the 'deleted' column will be populated
        with the timestamp of when the deletion event occurred. This would allow an admin to
        revert changes if required.
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            job_contact = JobContact.objects.get(pk=pk, job__user=current_user)
            contact = Contact.objects.get(pk=job_contact.contact_id)

            job_contact.delete()
            contact.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JobContact.DoesNotExist as ex:
            return Response({'reason': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Handle POST requests to create a new job contact record
        """

        current_user = User.objects.get(pk=request.auth.user.id)

        # Make sure the job we're adding the contact to belongs to the user
        try:
            job = Job.objects.get(pk=request.data['job'], user=current_user)
        except Job.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        contact = Contact()
        contact.first_name = request.data['first_name']
        contact.last_name = request.data['last_name']
        contact.phone = request.data['phone']
        contact.email = request.data['email']

        job_contact = JobContact()
        job_contact.contact = contact
        job_contact.job = job

        try:
            contact.save()
            job_contact.save()
            serializer = JobContactSerializer(
                job_contact, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return Response(ex.args[0], status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Handle PUT requests for a job contact
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            job_contact = JobContact.objects.get(pk=pk, job__user=current_user)
        except JobContact.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        contact = Contact.objects.get(id=job_contact.contact_id)

        contact.first_name = request.data['first_name']
        contact.last_name = request.data['last_name']
        contact.phone = request.data['phone']
        contact.email = request.data['email']
        contact.save()

        job_contact.contact = contact
        job_contact.save()

        serializer = JobContactSerializer(
            job_contact, context={'request': None})

        return Response(serializer.data)

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
