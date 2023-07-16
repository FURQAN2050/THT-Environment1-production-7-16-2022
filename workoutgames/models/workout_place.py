from django.db import models
from .media import ImageWorkout, VideoWorkout
from .tag import Tag
from .workout import Workout
from .movement import Movement

class WorkoutPlace(models.Model):

    """
    Workout at Home or the Gym

    Attributes:
        image_content(ManyToMany): Many To Many relationship with ImageWorkout model
        video_content(ManyToMany): Many To Many relationship with VideoWorkout model
        movements(ManyToMany): Many to Many relationship with Movement
        workout(ForeignKey): Many to one relationship with Workout

    """

    PLACE = [
        ('G','Gym'),
        ('H','Home'),
        ('B','Both')
    ]

    place = models.CharField(max_length=1, choices=PLACE, default='B')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    movements = models.ManyToManyField(Movement, blank=True)

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

        return self.workout.name + " " + self.place
