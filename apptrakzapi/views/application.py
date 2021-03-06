from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Application, ApplicationStatus, Job, Status


class ApplicationView(ViewSet):
    def list(self, request):
        """
        Handle GET requests to list all applications for the current user
        """

        current_user = User.objects.get(pk=request.auth.user.id)

        applications = Application.objects.filter(
            user=current_user).order_by('-submitted_at')

        for application in applications:
            application.job = Job.objects.get(pk=application.job_id)
            application.statuses = ApplicationStatus.objects.filter(
                application=application)

            for app_status in application.statuses:
                app_status.name = Status.objects.get(
                    pk=app_status.status_id)

        serializer = ApplicationSerializer(
            applications, many=True, context={'request': request}
        )

        return Response(serializer.data)


class ApplicationStatusSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.CharField()

    class Meta:
        model = ApplicationStatus
        fields = ('id', 'updated_at', 'reason', 'is_current', 'name')


class ApplicationJobSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Job
        fields = ('url', 'role_title')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):

    statuses = ApplicationStatusSerializer(many=True)
    job = ApplicationJobSerializer(many=False)

    class Meta:
        model = Application
        fields = ('id', 'submitted_at', 'is_active', 'statuses', 'job')
