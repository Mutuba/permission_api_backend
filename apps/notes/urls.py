from rest_framework import routers
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    NoteViewSet,
)

router = DefaultRouter(trailing_slash=False)

app_name = "notes"

urlpatterns = [

    path("", NoteViewSet.as_view({"post": "create"}), name="create_note"),
    path("list", NoteViewSet.as_view({"get": "list"}), name="fetch_notes"),
    path(
        "<int:pk>",
        NoteViewSet.as_view({"get": "retrieve"}),
        name="fetch_note",
    ),
    path(
        "<int:pk>/update",
        NoteViewSet.as_view({"put": "update"}),
        name="update_note",
    ),
    path(
        "<int:pk>/delete",
        NoteViewSet.as_view({"delete": "destroy"}),
        name="delete_note",
    ),
]
