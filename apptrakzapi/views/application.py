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

        # Return application statuses that are current
        # for the active user
        applicationStatuses = ApplicationStatus.objects.filter(
            application__user=current_user).order_by('-updated_at')

        serializer = ApplicationStatusSerializer(
            applicationStatuses, many=True, context={'request': request})

        return Response(serializer.data)


class ApplicationJobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('url', 'role_title')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):

    job = ApplicationJobSerializer(many=False)

    class Meta:
        model = Application
        fields = ('id', 'job', 'submitted_at', 'is_active')


class StatusSerializer(serializers.HyperlinkedModelSerializer):

    status = serializers.CharField(source='name')

    class Meta:
        model = Status
        fields = ('status',)


class ApplicationStatusSerializer(serializers.HyperlinkedModelSerializer):

    application_details = ApplicationSerializer(
        source='application', many=False)

    application_status = StatusSerializer(source='status', many=False)

    class Meta:
        model = ApplicationStatus
        fields = ('application_details', 'updated_at',
                  'reason', 'is_current', 'application_status')
