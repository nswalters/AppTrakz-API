from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Application, ApplicationStatus, Contact, Company, Job, JobContact, Status


class JobView(ViewSet):
    """ Job ViewSet """

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests for a job.

        The job record will be 'soft-deleted', i.e. the 'deleted' column will be populated
        with the timestamp of when the deletion event occurred. This would allow an admin to
        revert changes if required.
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            job = Job.objects.get(pk=pk, user=current_user)
            # job_contacts = JobContact.objects.filter(
            #     job=pk, job__user=current_user)

            # for contact in job_contacts:
            #     Contact.objects.get(pk=contact.contact_id).delete()

            job.delete()
            # job_contacts.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Job.DoesNotExist as ex:
            return Response({'reason': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Handle PUT operations for jobs
        """
        current_user = User.objects.get(pk=request.auth.user.id)
        job = Job.objects.get(pk=pk)

        # Make sure the company we're adding the job to belongs to the user
        try:
            company = Company.objects.get(
                pk=request.data["company"], user=current_user)
        except Company.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        job.company = company
        job.role_title = request.data["role_title"]
        job.type = request.data["type"]
        job.qualifications = request.data["qualifications"]
        job.post_link = request.data["post_link"]  # Requires 'clean_fields()'
        job.description = request.data["description"]

        if "salary" in request.data:
            job.salary = request.data["salary"]

        # Validate job details and serialize
        try:
            job.clean_fields()
            job.save()
            serializer = NewJobSerializer(job, context={'request': None})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response(ex.args[-1], status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """ Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Make sure the company we're adding the job to belongs to the user
        try:
            company = Company.objects.get(
                pk=request.data["company"], user=current_user)
        except Company.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        job = Job()
        job.user = current_user
        job.company = company
        job.role_title = request.data["role_title"]
        job.type = request.data["type"]
        job.qualifications = request.data["qualifications"]
        job.post_link = request.data["post_link"]  # Requires 'clean_fields()'
        job.description = request.data["description"]

        if "salary" in request.data:
            job.salary = request.data["salary"]

        # Validate job details and serialize
        try:
            job.clean_fields()
            job.save()
            serializer = NewJobSerializer(job, context={'request': None})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response(ex.args[0], status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Handle GET requests to list all jobs for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Return jobs sorted alphabetically
        jobs = Job.objects.filter(user=current_user).order_by('role_title')

        # Add application and application status details to each job result
        for job in jobs:
            try:
                job.application = Application.objects.get(job=job)
                job.application.current_status = ApplicationStatus.objects.get(
                    application=job.application, is_current=True)
            except Exception:
                job.application = None

        serializer = JobSerializer(
            jobs, many=True, context={'request': None})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            job = Job.objects.get(pk=pk)

            try:
                job.application = Application.objects.get(job=job)
                job.application.current_status = ApplicationStatus.objects.get(
                    application=job.application, is_current=True)
            except Exception:
                job.application = None

            serializer = JobSerializer(job, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


class NewJobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'url', 'company', 'role_title', 'type',
                  'qualifications', 'post_link', 'salary', 'description')


class JobCompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'url', 'name')


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('name',)


class JobApplicationStatusSerializer(serializers.HyperlinkedModelSerializer):

    status = StatusSerializer(many=False)

    class Meta:
        model = ApplicationStatus
        fields = ('updated_at', 'reason', 'is_current', 'status')


class JobApplicationSerializer(serializers.HyperlinkedModelSerializer):

    current_status = JobApplicationStatusSerializer(many=False)

    class Meta:
        model = Application
        fields = ('submitted_at', 'is_active', 'current_status')


class JobSerializer(serializers.HyperlinkedModelSerializer):

    company = JobCompanySerializer(many=False)
    application = JobApplicationSerializer(many=False)

    # TODO: Need to add 'contacts' to this at somepoint
    class Meta:
        model = Job
        fields = ('id', 'url', 'role_title', 'company', 'type',
                  'qualifications', 'post_link', 'salary', 'description', 'application')
