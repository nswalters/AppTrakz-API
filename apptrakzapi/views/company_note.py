from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Company, CompanyNote
from apptrakzapi.views.company import CompanySerializer


class CompanyNoteView(ViewSet):
    def create(self, request):
        """
        Handle POST requests to create new company note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Make sure that the company we're adding a note to belongs to the user
        try:
            company = Company.objects.get(
                pk=request.data['company'], user=current_user)
        except Company.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note = CompanyNote()
        note.author = current_user
        note.company = company
        note.content = request.data['content']

        note.save()

        serializer = CompanyNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for a specific company note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            company_note = CompanyNote.objects.get(pk=pk, author=current_user)

            serializer = CompanyNoteSerializer(
                company_note, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to list all company notes for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        company_notes = CompanyNote.objects.filter(author=current_user)

        serializer = CompanyNoteSerializer(
            company_notes, many=True, context={'request': None})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Handle PUT requests for a company note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Verify the current user is the author of the note
        try:
            note = CompanyNote.objects.get(pk=pk, author=current_user)
        except CompanyNote.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note.content = request.data['content']

        note.save()

        serializer = CompanyNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests for a company note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            note = CompanyNote.objects.get(pk=pk, author=current_user)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CompanyNote.DoesNotExist as ex:
            return Response({'reason': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class CompanyNoteAuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class CompanyNoteSerializer(serializers.HyperlinkedModelSerializer):

    author = CompanyNoteAuthorSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = CompanyNote
        fields = ('content', 'created_at', 'author', 'company')
