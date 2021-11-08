import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.authentication.serializers import UserSerializer
from .models import Note



class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    like = serializers.SerializerMethodField(method_name="get_like_count")
    dislike = serializers.SerializerMethodField(method_name="get_dislike_count")
    created_at_date = serializers.SerializerMethodField(method_name="get_created_at")
    updated_at_date = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Note
        fields = (
            "id",
            "author",
            "body",
            "tagList",
            "created_at_date",
            "description",
            "slug",
            "title",
            "updated_at_date",
            "like",
            "dislike",
        )
        
    def get_created_at(self, instance):
        # Returns the date when article was created in isoformat()
        # Example:
        # date(2002, 12, 4).isoformat() == '2002-12-04'.
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        # Returns the date when an article was updated in isoformat()
        # Example:
        # date(2002, 12, 4).isoformat() == '2002-12-04'.

        return instance.updated_at.isoformat()
    
    def get_like_count(self, obj):
        """Sets the value of like field to the serializer
        by returning the length of the like object."""
        # counts the number of children the like object has
        return obj.like.count()

    def get_dislike_count(self, obj):
        """Sets the value of dislike field to the
        serializer by returning the length of the dislike object."""
        # counts the number of children the dislike object has
        return obj.dislike.count()

    def create(self, validated_data):
        """Method creates an article based on validated data"""
        note = Note.objects.create(**validated_data)
        return note