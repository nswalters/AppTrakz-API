from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Application, ApplicationStatus, Job, Status


class ApplicationView(ViewSet):
    def update(self, request, pk=None):
        """
        Handle PUT requests to update an application
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Verify application we are editing belongs to this user
        try:
            new_application = Application.objects.get(pk=pk, user=current_user)
        except Application.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # Application model
        new_application.is_active = request.data["is_active"]

        # ApplicationStatus model
        #
        # Need to complete a few steps here

        # 1 - Get the current status record and set that `is_current` value to False
        current_app_status = ApplicationStatus.objects.get(
            application=new_application, is_current=True)
        current_app_status.is_current = False

        # 2 - Get the new status selected
        new_status = Status.objects.get(pk=request.data["status"])

        new_app_status = ApplicationStatus()
        new_app_status.status = new_status
        new_app_status.is_current = True
        new_app_status.application = new_application

        # 3 - Set the 'reason' and 'status' values accordingly on our application_status
        if "reason" in request.data:
            new_app_status.reason = request.data["reason"]

        # Try and save all the records, but if any one operation fails,
        # error out and don't do any of them.
        try:
            new_application.save()
            current_app_status.save()
            new_app_status.save()

        except ValidationError as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        # Get the final application
        full_application = Application.objects.get(pk=new_application.id)

        # Append application statuses
        full_application.statuses = ApplicationStatus.objects.filter(
            application=full_application)

        # Append status name
        for app_status in full_application.statuses:
            app_status.name = Status.objects.get(pk=app_status.status_id)

        serializer = ApplicationSerializer(
            full_application, context={'request': None})

        return Response(serializer.data)

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
                application=application).order_by('-updated_at')

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
        fields = ('id', 'updated_at', 'reason',
                  'is_current', 'name', 'created_at')


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
