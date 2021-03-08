from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Application, ApplicationStatus, Job, Status


class ApplicationView(ViewSet):
    def create(self, request):
        """
        Handle POST requests to create a new application
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Verify the job we are applying to exists for this user
        try:
            job = Job.objects.get(
                pk=request.data["job"], user=current_user)
        except Job.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # Create Application instance
        new_application = Application()
        new_application.user = current_user
        new_application.job = job

        # Creating a new application means it's automatically active
        new_application.is_active = True

        # Verify the user has not already applied to that job
        # i.e. Violates unique constraint on application table (user & job)
        try:
            new_application.save()
        except IntegrityError as ex:
            return Response({"reason": "You've already applied to that job."}, status=status.HTTP_400_BAD_REQUEST)

        # Create ApplicationStatus instance
        new_app_status = ApplicationStatus()
        new_app_status.application = new_application

        # The first status will always be a 'New Application'
        new_app_status.reason = "New Application"

        # Defaults to the 'Applied' status
        new_app_status.status = Status.objects.get(name='Applied')

        # Default to 'True' as this is a brand new application
        new_app_status.is_current = True

        new_app_status.save()

        # Get the final application
        full_application = Application.objects.get(
            pk=new_application.id)

        # Append application statuses
        full_application.statuses = ApplicationStatus.objects.filter(
            application=full_application)

        # Append status name
        for app_status in full_application.statuses:
            app_status.name = Status.objects.get(name='Applied')

        serializer = ApplicationSerializer(
            full_application, many=False, context={'request': None}
        )

        return Response(serializer.data)

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
            applications, many=True, context={'request': None}
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
        fields = ('id', 'url', 'role_title')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):

    statuses = ApplicationStatusSerializer(many=True)
    job = ApplicationJobSerializer(many=False)

    class Meta:
        model = Application
        fields = ('id', 'submitted_at', 'is_active', 'statuses', 'job')
