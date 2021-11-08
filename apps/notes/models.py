import os
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


from apps.authentication.models import User


class TimestampedModel(models.Model):
    """Model to take care of when an instance occurs in the database
    Appends created at and updated at fields using datetime.now()"""

    # Timestamp shows when an object was first created in the database
    created_at = models.DateTimeField(auto_now_add=True)

    # represents when an object was last changed

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # It is a good practice to have ordering in reverse chronology.
        #
        ordering = ["-created_at", "-updated_at"]


class Note(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    tagList = ArrayField(
        models.CharField(max_length=255), default=None, null=True, blank=True
    )
    # blank = True
    # a many-to-many field will map to a serializer field that
    # requires at least one input, unless the model field has blank=True
    like = models.ManyToManyField(User, blank=True, related_name="like")
    # define related_name argument for 'Note.like' or 'Note.dislike'.
    # to ensure that the fields were not conflicting with each other,
    dislike = models.ManyToManyField(User, blank=True, related_name="dislike")
    # An author is the creator of the article, usually the current logged in user.
    # I create a foreign key r/ship.
    # This r/ship can help returns all note of a particular author.
    author = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="notes"
    )
    ratings_counter = models.IntegerField(default=0)

    prepopulated_fields = {"slug": ("title",)}

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Note.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        """Creates a slug based on Note title
        Example:
        Title: NoteOne
        Slug: NoteOne-1
        """
        self.slug = self._get_unique_slug()
        super(Note, self).save(*args, **kwargs)

    def updaterate(self, rating):
        """ """
        self.ratings_counter = rating

    def __str__(self):
        """Returns a title of the note as object representation"""

        return self.title


class NoteRating(models.Model):
    """
    Defines the ratings fields for a rater

    """

    rater = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="ratings"
    )
    note_text = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="noteratings")
    rating = models.IntegerField()

    def __str__(self):
        return self.note_text
