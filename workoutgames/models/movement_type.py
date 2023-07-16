from django.db import models
from .media import ImageWorkout, VideoWorkout
from .tag import Tag
from django.utils import timezone

class MovementType(models.Model):

    """
    Model to represent a type of movement

    Attributes:
        name(String)
        description(String)
        datePosted(DateTimeField)
        tag(ManyToManyField): Many To Many relationship with Tag
        image_content(ManyToMany): Many To Many relationship with ImageWorkout model
        video_content(ManyToMany): Many To Many relationship with VideoWorkout model

    """

    name = models.CharField(max_length=50)
    description = models.TextField()
    datePosted = models.DateTimeField()
    tag = models.ManyToManyField(Tag)
    #image_content = models.ManyToManyField(ImageWorkout, blank=True)
    video_content = models.CharField(max_length=1000, default=None, null=True)
    #thumbnail_movement = models.ForeignKey(ImageWorkout, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='thumbnail_assigned')

    class Meta:
        ordering = ('name',)

    def __str__(self):

        """
        Returns name of movement type as string
        """

        return self.name

    

    def save(self, *args, **kwargs):

        """
        Sets posted date for object
        """

        if not self.id:
            self.datePosted = timezone.now()

        super(MovementType, self).save(*args, **kwargs)