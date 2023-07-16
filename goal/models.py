from django.db import models
from accounts.models import User


# Create your models here.

class MyGoal(models.Model):

    """
    Model to represent a goal for teachers

    Attributes:

        goal(String)
        User(OneToOne): One to one field to User

    """

    MAX_GOAL_LEN = 200

    goal = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.goal

    @staticmethod
    def setGoal(user, goal):

        """
        Sets goal for user
        
        Parameters:
            goal(String): Under 200 characters

        Returns:
            Boolean - True if goal was set, False otherwise

        """

        if len(goal) > MyGoal.MAX_GOAL_LEN:
            return False

        goalInstance = MyGoal.objects.filter(user = user)

        if len(goalInstance) == 0:
            goalInstance = MyGoal(user = user)

        else:
            goalInstance = goalInstance[0]

        goalInstance.goal = goal
        goalInstance.save()

        return True
