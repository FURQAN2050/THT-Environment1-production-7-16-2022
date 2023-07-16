from django.db import models
from .media import ImageWorkout, VideoWorkout
from .tag import Tag
from django.utils import timezone

class Workout(models.Model):

    """
    Model to represent a workout

    Attributes:

        name(String)
        description(String)
        datePosted(DateTimeField)
        level(Integer)
        tag(ManyToManyField): Many To Many relationship with Tag
        image_content(ManyToMany): Many To Many relationship with ImageWorkout model
        video_content(ManyToMany): Many To Many relationship with VideoWorkout model
        points(Integer): Points that users will earn based on completing this workout
        slug(SlugField): Unique link identifier

    """

    name = models.CharField(max_length=50)
    description = models.TextField()
    datePosted = models.DateTimeField()
    level = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)
    image_content = models.ManyToManyField(ImageWorkout, blank=True)
    video_content = models.ManyToManyField(VideoWorkout, blank=True)
    points = models.IntegerField(default=1)

    def getThumbnail(self):

        """
            Gets thumbnail from media
        """

        if len(self.image_content.all()) > 0:
            return self.image_content.all()[0].thumbnail.url

        elif len(self.video_content.all()) > 0:
            return self.video_content.all()[0].thumbnail.url
        
        else:
            return None

    def __str__(self):

        """
        Returns name of workout as string
        """

        return self.name


    def save(self, *args, **kwargs):

        """
        Sets posted date for object
        """

        if not self.id:
            self.datePosted = timezone.now()

        super(Workout, self).save(*args, **kwargs)