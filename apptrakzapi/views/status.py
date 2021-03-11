from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Status


class StatusView(ViewSet):
    """
    Handle GET requests to list all statuses
    """

    def list(self, request):
        statuses = Status.objects.all()

        serializer = StatusSerializer(
            statuses, many=True, context={'request': None})

        return Response(serializer.data)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name')
