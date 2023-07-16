from django.db import models
from content.models import Tag
from django.utils import timezone
from .workout import Workout
from .pathInstance import PathInstance
from .media import ImageWorkout

class Path(models.Model):

    """
    Model to represent a Path of workouts

    Attributes:

        name(String)
        description(String)
        workout(ManyToManyField): Many To Many relationship with Workout
        levelPath(Integer): Level corresponding to the path

    """

    name = models.CharField(max_length=50)
    description = models.TextField()
    workout = models.ManyToManyField(Workout)
    levelPath = models.IntegerField(default=1)
    thumbnail_path = models.ForeignKey(ImageWorkout, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='thumbnail_assigned')
    sortOrder = models.IntegerField(default=100)

    def createPathInstance(self):

        """
        Creates a PathInstance associated with current Path

            PathInstance.currentLevel is set to 1

        Parameters: 
            Void
          
        Returns: 
            PathInstance: Created instance (already saved to database)
        """

        pathInstance = PathInstance()
        pathInstance.currentLevel = 1
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = self

        pathInstance.save()

        return pathInstance
        
        

    def canUserAccessWorkout(self, gamer, workout):

        """
        Checks whether gamer can access a specific workout

            Workout must be in path.workout

        Parameters: 
            gamer(Gamer): Gamer that is attempting to access workout
            workout(Workout): Workout that is being accessed
          
        Returns: 
            Boolean: True if gamer can access workout, False otherwise
        """

        pathInstance = PathInstance.objects.filter(gamer=gamer, path=self)

        if len(pathInstance) > 0:

            pathInstance = pathInstance[0]

            if pathInstance.currentLevel >= workout.level:

                return True

        return False

    def canUserAccessPath(self, gamer):

        """
        Checks whether gamer can access current path

        Parameters: 
            gamer(Gamer): Gamer that is attempting to access workout
          
        Returns: 
            Boolean: True if gamer can access path, False otherwise
        """

        if gamer.currLevelPath >= self.levelPath:

            return True

        return False


    def getThumbnail(self):

        """
        Gets thumbnail from media in first workout
        """

        # if len(self.workout.all()) > 0:

        #     workout = self.workout.all()[0]

        #     if len(workout.image_content.all()) > 0:
        #         return workout.image_content.all()[0].thumbnail.url

        #     elif len(workout.video_content.all()) > 0:
        #         return workout.video_content.all()[0].thumbnail.url
        
        # return None

        if self.thumbnail_path != None:
            return self.thumbnail_path.image_field.url

        else:
            return None

    def __str__(self):

        """
        Returns name of path as string
        """

        return self.name

