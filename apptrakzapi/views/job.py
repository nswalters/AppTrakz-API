from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Application, ApplicationStatus, Company, Job, Status


class JobView(ViewSet):

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


class JobCompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('url', 'name')


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
