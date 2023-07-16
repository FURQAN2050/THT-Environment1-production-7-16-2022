import pytz
from django.db import models
from django.utils import timezone
from accounts.models import User
from .pathInstance import PathInstance
from .workout import Workout
from .path import Path
from .movement_instance import MovementInstance

import pdb

class Gamer(models.Model):

    """
    Model that represents a Gamer

    Attributes:
        User(OneToOne): One to one field to User
        PathInstance(OneToMany): One to many field to PathInstance
        currLevelPath(Integer): Gamer level based on paths completed
        dailyCompletedWorkouts(Integer): Amount of workouts completed in a day
        dailyTimestampWorkoutCompleted(Date): Date of last completed workout
        accessedPath(PathInstance): Foreign Key relationship with PathInstance

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    path = models.ManyToManyField(PathInstance)
    currLevelPath = models.IntegerField(default=1)
    dailyCompletedWorkouts = models.IntegerField(default=0)
    dailyTimestampWorkoutCompleted = models.DateField(default=timezone.datetime(2020, 1, 1).date())
    accessedPath = models.ForeignKey(Path, null=True, on_delete=models.SET_DEFAULT, default=None)


    def accessPath(self, path):
        
        """
        Associates gamer with a Path to store workouts completed and levels

        Parameters: 
            path(Path): Path to access
          
        Returns: 
            Boolean: True if accessPath was successful, False otherwise
        """

        if path.canUserAccessPath(self): # and self.checkAccessedPath(path):

            pathInstanceFilter = PathInstance.objects.filter(path=path, gamer=self)

            if len(pathInstanceFilter) <= 0:

                pathInstance = path.createPathInstance()
                self.path.add(pathInstance)
            
            self.accessedPath = path
            self.save()

            return True

        return False


    def getPathInstance(self, path):

        """
        Obtains the latest path instance associated with the user corresponding
        to a specific path

        Patameters:
            path(Path): Path to get instance from

        Returns:
            PathInstance: Latest path instance from user corresponding to path. 
            None if no path instance exists
        """

        path_instance = PathInstance.objects.filter(path=path, gamer__in=[self]).order_by('-dateStarted')

        if len(list(path_instance)) > 0:
            path_instance = path_instance[0]
        else:
            path_instance = None

        return path_instance

    def getMovementInstance(self, movement, path_instance):

        """
        Gets a specific movement instance

        Parameters:
            movement(Movement) - Movement to get instance from
            path_instance(PathInstance) - PathInstance to get movement from

        Returns:
            MovementInstance: Movement instance from path. None if movement
            has not been accessed
        """

        movement_instance = MovementInstance.objects.filter(path_instance=path_instance, movement=movement)

        if len(list(movement_instance)) > 0:
            movement_instance = movement_instance[0]
        else:
            movement_instance = None

        return movement_instance

    
    def isMovementAccessed(self, movement, path_instance):

        """
        Returns True if path was accessed by gamer and False otherwise

        Parameters: 
            myPath(Path): Path to check
          
        Returns: 
            Boolean: True if path was accessed by gamer False otherwise

        """

        movement_instance = self.getMovementInstance(movement, path_instance)

        if movement_instance == None:
            return False
        else:
            return True


    def accessMovement(self, movement, path):

        """
        Creates a movement instance and associates it with the gamer

        Parameter:
            movement(Movement): Movement to access

        Returns:
            MovementInstance
        """

        path_instance = self.getPathInstance(path)
        movement_instance = MovementInstance.objects.filter(movement__id=movement.id, path_instance__id=path_instance.id)

        if len(list(movement_instance)) > 0:
            movement_instance = movement_instance[0]

        else:
            movement_instance = MovementInstance(movement=movement, path_instance=path_instance)
            movement_instance.save()

        return movement_instance



    def checkAccessedPath(self, path):

        """
        Keeps user at only one path at a time

        Parameters:
            path(Path): Path to access

        Returns
            Boolean: True if user can access path, False otherwise
        
        """

        canAccess = True
        localAccessedPath = self.accessedPath

        if localAccessedPath == None:
            localAccessedPath = path

        elif localAccessedPath != path:

            pathInstance = self.getPathInstance(self.accessedPath)

            if pathInstance.isPathComplete():
                canAccess = True
            else:
                canAccess = False

        return canAccess


    def completeWorkout(self, myPath, workout, testing=False):

        # TODO

        """
        Marks a workout from a path as completed. *** If a workout completes a path
        then gamer currLevelPath will increase by 1

        Parameters: 
            myPath(Path): Path to access
            workout(Workout): Workout that was completed
          
        Returns: 
            Boolean: True if process was successful
        """

        pathInstance = self.getPathInstance(myPath)

        if pathInstance == None:
            raise Exception(err)
        
        workoutFilter = Workout.objects.filter(id=workout.id).filter(pathinstance__in=[pathInstance])


        # Determine if workout can be completed

        if (len(workoutFilter) <= 0 
        and myPath.canUserAccessWorkout(self, workout) 
        and self.checkMaxWorkoutsPerDay(testing)):

            pathInstance.addWorkout(workout)

            workoutLevelFilter = Workout.objects.filter(path__in=[myPath]).filter(level=workout.level)
            pathInstanceWorkout = Workout.objects.filter(pathinstance__in=[pathInstance]).filter(level=workout.level)

            intersect = set(pathInstanceWorkout.all())

            #intersect.intersection(pathInstanceWorkout.all())

            if len(intersect) == len(workoutLevelFilter.all()):

                pathInstance.currentLevel = pathInstance.currentLevel + 1
                pathInstance.save()

            # Increase points

            self.user.teacher.addPoints(workout.points, timezone.now().date().strftime("%m/%d/%Y"))

            # Increment Max Workouts

            self.updateWorkoutsPerDay()

            # Determine whether to increase currPathLevel

            #pdb.set_trace()

            pathsLevel = Path.objects.filter(levelPath=myPath.levelPath)
            pathsCompletedLevel = PathInstance.objects.isCompleted(myPath.levelPath, self)

            #if len(pathsLevel.all()) == len(pathsCompletedLevel):
            if pathInstance.isPathComplete() == True:

                if myPath.levelPath >= self.currLevelPath:

                    self.currLevelPath = myPath.levelPath + 1

                    self.save()

        else:

            return False

        return True

    def setDateToday(self):

        """
        Sets dailyTimestampWorkoutCompleted to today

        """

        currentZone = pytz.timezone(self.user.timezone)

        self.dailyTimestampWorkoutCompleted = timezone.localdate(timezone=currentZone)

        self.save()


    def checkMaxWorkoutsPerDay(self, bypass=False):

        if bypass:
            return True

        currentZone = pytz.timezone(self.user.timezone)
        today = timezone.localdate(timezone=currentZone)

        if self.dailyCompletedWorkouts < 2 or self.dailyTimestampWorkoutCompleted < today:

            return True

        else:

            return False


    def updateWorkoutsPerDay(self):

        currentZone = pytz.timezone(self.user.timezone)
        today = timezone.localdate(timezone=currentZone)

        if self.dailyTimestampWorkoutCompleted < today:

            self.dailyTimestampWorkoutCompleted = today
            self.dailyCompletedWorkouts = 1

        else:

            if self.dailyCompletedWorkouts < 2:
                
                self.dailyCompletedWorkouts += 1

        self.save()


    def isPathAccessed(self, myPath):

        """
        Returns True if path was accessed by gamer and False otherwise

        Parameters: 
            myPath(Path): Path to check
          
        Returns: 
            Boolean: True if path was accessed by gamer False otherwise

        """


        if len(PathInstance.objects.filter(gamer__in=[self]).filter(path__in=[myPath])) > 0:
            return True

        else:
            return False

    def isWorkoutComplete(self, myPath, workout):

        """
        Returns True if a workout from a path has been completed and False otherwise

        Parameters: 
            myPath(Path): Path to check
            workout(Workout): Workout to check
          
        Returns: 
            Boolean: True if workout was completed False otherwise

        """

        if self.isPathAccessed(myPath):

            pathInstance = PathInstance.objects.get(gamer__in=[self], path__in=[myPath])

            if len(Workout.objects.filter(pathinstance__in=[pathInstance]).filter(id=workout.id)) > 0:

                return True
        
        return False
        

            



            

            

            