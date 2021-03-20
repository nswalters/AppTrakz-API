from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apptrakzapi.models import Contact, ContactNote, JobContact


class ContactNoteView(ViewSet):
    def create(self, request):
        """
        Handle POST requests to create new contact note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Make sure that the contact we're adding a note to belongs to the user
        try:
            contact = Contact.objects.get(
                pk=request.data['contact'])
            job_contact = JobContact.objects.get(
                job__user=current_user, contact=contact)
        except JobContact.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note = ContactNote()
        note.author = current_user
        note.contact = contact
        note.content = request.data['content']

        note.save()

        serializer = ContactNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for a specific contact note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            contact_note = ContactNote.objects.get(pk=pk, author=current_user)

            serializer = ContactNoteSerializer(
                contact_note, context={'request': None})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests to list all contact notes for the current user
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        contact_notes = ContactNote.objects.filter(
            author=current_user).order_by('created_at')

        serializer = ContactNoteSerializer(
            contact_notes, many=True, context={'request': None})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Handle PUT requests for a contact note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        # Verify the current user is the author of the note
        try:
            note = ContactNote.objects.get(pk=pk, author=current_user)
        except ContactNote.DoesNotExist as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        note.content = request.data['content']

        note.save()

        serializer = ContactNoteSerializer(note, context={'request': None})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handle DELETE requests for a contact note
        """
        current_user = User.objects.get(pk=request.auth.user.id)

        try:
            note = ContactNote.objects.get(pk=pk, author=current_user)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ContactNote.DoesNotExist as ex:
            return Response({'reason': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ContactNoteContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name')


class ContactNoteAuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ContactNoteSerializer(serializers.HyperlinkedModelSerializer):

    author = ContactNoteAuthorSerializer(many=False)
    contact = ContactNoteContactSerializer(many=False)

    class Meta:
        model = ContactNote
        fields = ('id', 'content', 'created_at', 'author', 'contact')
