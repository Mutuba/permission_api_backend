from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Note
from functools import partial
from .serializers import NoteSerializer
from rest_framework.exceptions import NotFound
from rest_framework import mixins, status, viewsets
from apps.core.permissions import UserHasPermission

class NoteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    By subclassing create, list, retrieve and destroy
    we can define create, list, retrieve and destroy
    endpoints in one class
    """

    lookup_field = "slug"
    queryset = Note.objects.all()
    permission_classes = [
        IsAuthenticated,
        partial(UserHasPermission, "can_create_note"),
    ]
    serializer_class = NoteSerializer

    @swagger_auto_schema(
        operation_description="Create Note", operation_id="note_create"
    )
    def create(self, request):

        """Creates a new article in the database
        Method takes user data, validates and commits in the db
        """
        serializer_data = request.data

        serializer = self.serializer_class(
            data=serializer_data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Get a list Note", operation_id="notes_list"
    )
    def list(self, request):

        """Retrives all notes from the database
        with the latest to be created first
        (chronologically)
        """

        serializer_context = {"request": request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(page, context=serializer_context, many=True)

        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get a Note by id", operation_id="fetch_note"
    )
    def retrieve(self, request, pk=None):

        """
        Method returns a single note
        Takes a slug as unique identifier, searches the db
        and returns an note with matching slug.
        Returns NotFound if a note does not exist
        """

        serializer_context = {"request": request}

        try:
            note = Note.objects.get(id=pk)
        except Note.DoesNotExist:

            raise NotFound("a Note with this slug does not exist.")

        serializer = self.serializer_class(note, context=serializer_context)

        return Response({"note": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):

        """Method updates partially a single note
        Takes a pk as unique identifier, searches the db
        and updates an note with matching slug.
        Returns NotFound if an note does not exist"""

        serializer_context = {"request": request}

        try:
            serializer_instance = self.queryset.get(id=pk)
        except Note.DoesNotExist:

            raise NotFound("A note with this slug does not exist.")

        serializer_data = request.data

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True,
        )
        note = Note.objects.get(id=pk)

        if request.user != note.author:
            return Response(
                {"message": "You can only update your article"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
           note = self.queryset.get(id=pk)

        except Note.DoesNotExist:
            raise NotFound("An note with this slug does not exist.")

        if request.user != note.author:
            return Response(
                {"message": "You can only delete your note"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if note.delete():
            return Response(
                {"message": "You have successfully deleted the note"},
                status=status.HTTP_200_OK,
            )