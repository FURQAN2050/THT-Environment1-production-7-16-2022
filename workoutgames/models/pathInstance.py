from django.db import models
from .workout import Workout

class PathInstanceManager(models.Manager):

    def isCompleted(self, level, gamer):

        result_list = []

        pathInstances = PathInstance.objects.filter(path__levelPath=level, gamer__in=[gamer])

        for pathInstance in pathInstances.all():

            if pathInstance.isPathComplete() == True:

                result_list.append(pathInstance)

        result_list = set(result_list)

        return result_list



class PathInstance(models.Model):

    """
    Model to represent the paths taken by each individual Gamer

    UserInstances = PathInstance if UserInstances not constains PathInstance

    Attributes:

        currentLevel(Integer)
        dateStarted(DateTimeField): For started path
        workout(ManyToMany): Field with finished Workouts
        path(foreignKey): Field with Path
        gamer(foreignKey): Field with Gamer

    """

    currentLevel = models.IntegerField(default=0)
    dateStarted = models.DateTimeField()
    workout = models.ManyToManyField(Workout)
    path = models.ForeignKey('Path', on_delete=models.CASCADE)

    objects = PathInstanceManager()


    def addWorkout(self, workoutToAdd):

        """
        Adds a workout to the list of workouts completed

        Parameters: 
            workout(Workout): Workout just completed
          
        Returns: 
            Boolean: True if workout was added successfully, False otherwise
        """


        try:
            
            self.workout.add(workoutToAdd)
            self.save()
            return True

        except:

            raise Exception("Workout not added properly")


    def isPathComplete(self):

        workoutsCompleted = self.workout.all().count()
        workoutsAvailable = self.path.workout.all().count()

        if workoutsCompleted >= workoutsAvailable:

            return True
        
        else:

            return False

            

    def isWorkoutComplete(self, workout):

        workouts = self.workout.filter(id=workout.id)

        if workouts.all().count() > 0:

            return True
        
        else:

            return False

        
