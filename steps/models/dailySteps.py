from django.db import models
from django.utils import timezone


class DailySteps(models.Model):

    """
    Model that represents a day of steps

    Attributes:
        User(OneToOne): One to one field to User
        numSteps(Integer): Amount of steps in that day
        date(Date): Date

    """

    stepsCompetitor = models.ForeignKey('StepsCompetitor', on_delete=models.CASCADE)
    dailySteps = models.IntegerField()
    date = models.DateField(default=timezone.now().date())

    def setSteps(self, steps):

        """
        Set number of steps

        Parameters:
            steps(Integer)

        Returns:
            Void

        """

        if int(steps) < 0:
            raise Exception()

        self.dailySteps = steps

        print(self.dailySteps)


