from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Status


class StatusView(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            status = Status.objects.get(pk=pk)
            serializer = StatusSerializer(status, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class StatusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Status
        fields = ('name',)
