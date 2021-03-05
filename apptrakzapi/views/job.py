from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company, Job


class JobView(ViewSet):

    def list(self, request):
        """
        Handle GET requests to list all jobs for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Return jobs sorted alphabetically
        jobs = Job.objects.filter(user=current_user).order_by('role_title')

        serializer = JobSerializer(
            jobs, many=True, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class JobCompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = ('url', 'name')


class JobSerializer(serializers.HyperlinkedModelSerializer):

    company = JobCompanySerializer(many=False)

    # Need to add 'contacts', application status,
    # and if 'active' items to this at somepoint
    # (i.e. after I get the details view going)
    class Meta:
        model = Job
        fields = ('id', 'role_title', 'company', 'type',
                  'qualifications', 'post_link', 'salary', 'description', 'url')
