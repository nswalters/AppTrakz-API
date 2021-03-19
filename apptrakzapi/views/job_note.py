from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Job, JobNote
from apptrakzapi.views.job import JobSerializer


class JobNoteView(ViewSet):
    def create(self, request):
        """
        Handle POST requests to create new job note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Make sure that the job we're adding a note to belongs to the user
        try:
            job = Job.objects.get(
                pk=request.data['job'], user=current_user)
        except Job.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note = JobNote()
        note.author = current_user
        note.job = job
        note.content = request.data['content']

        note.save()

        serializer = JobNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for a specific job note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            job_note = JobNote.objects.get(pk=pk, author=current_user)

            serializer = JobNoteSerializer(
                job_note, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to list all job notes for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        job_notes = JobNote.objects.filter(
            author=current_user).order_by('created_at')

        serializer = JobNoteSerializer(
            job_notes, many=True, context={'request': None})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Handle PUT requests for a job note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Verify the current user is the author of the note
        try:
            note = JobNote.objects.get(pk=pk, author=current_user)
        except JobNote.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note.content = request.data['content']

        note.save()

        serializer = JobNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests for a job note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            note = JobNote.objects.get(pk=pk, author=current_user)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JobNote.DoesNotExist as ex:
            return Response({'reason': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class JobNoteAuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class JobNoteSerializer(serializers.HyperlinkedModelSerializer):

    author = JobNoteAuthorSerializer(many=False)

    class Meta:
        model = JobNote
        fields = ('id', 'content', 'created_at', 'author')
