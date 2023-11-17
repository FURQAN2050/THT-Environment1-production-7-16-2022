from django.db import models
from django.utils import timezone

from accounts.models import User
from .dailySteps import DailySteps

from collections import OrderedDict

class StepsCompetitor(models.Model):

    """
    Model that represents a Steps Competitor

    Attributes:
        User(OneToOne): One to one field to User
        dailySteps(StepsDay): List of steps per day

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    totalSteps = models.IntegerField(default=0)

    def __calculateTotalSteps__(self):

        """
        Calculates total steps

        Parameters: 
            Void
          
        Returns: 
            Integer: Number of total steps
        """

        totalSteps = 0

        dailySteps = DailySteps.objects.filter(stepsCompetitor=self)

        for day in dailySteps:
            totalSteps += day.dailySteps

        return totalSteps


    def getTotalSteps(self):

        """
        Gets total steps

        Parameters: 
            Void
          
        Returns: 
            Integer: Number of total steps
        """


        return self.totalSteps


    def getStepsFromDay(self, date):

        """
        Gets total steps from a day

        Parameters: 
            date(Date)
          
        Returns: 
            Integer: Number of steps
        """

        totalSteps = 0
        dailyStepsDate = DailySteps.objects.filter(stepsCompetitor=self, date=date)

        for day in dailyStepsDate:
            totalSteps += day.dailySteps

        return totalSteps


    def recordSteps(self, steps, date,user):

        """
        Record steps for a specific date and updates total steps

        Parameters:
            steps(Integer): Number of steps to record
            date(Date)
          
        Returns: 
            Void
        """
        stepInstanceAlreadyExist=False;
        dailyStepsInstance = DailySteps.objects.filter(stepsCompetitor=self, date=date)

        if len(dailyStepsInstance) == 0:
            dailyStepsInstance = DailySteps(stepsCompetitor=self, date=date)
        else:
            dailyStepsInstance = dailyStepsInstance[0]
            print(dailyStepsInstance.dailySteps);
            stepInstanceAlreadyExist=True;

        
        print(stepInstanceAlreadyExist)

        if stepInstanceAlreadyExist==True:
            if dailyStepsInstance.addExtraPoints==True:
                if not (int(dailyStepsInstance.dailySteps)>=10000):
                    if (int(steps)>=10000):
                        print('adding points on the basis of first Condition');   
                        user.teacher.addPoints(25, timezone.now().date().strftime("%m/%d/%Y"))
                        dailyStepsInstance.setExtraPointsBool(False)
        
        if stepInstanceAlreadyExist==False:
            if(int(steps)>=10000):
                print('adding points on the basis of second Condition');   
                user.teacher.addPoints(25, timezone.now().date().strftime("%m/%d/%Y"))
                dailyStepsInstance.setExtraPointsBool(False)
                
        dailyStepsInstance.setSteps(steps)
        dailyStepsInstance.save()
        self.totalSteps = self.__calculateTotalSteps__()
        self.save()

    def getPlaceCurrent(self):

        """
        Get current place for user

        Parameters:
            Void
          
        Returns: 
            Integer - Place for user
        """

        competitors = StepsCompetitor.objects.only('totalSteps')
        stepsSet = OrderedDict.fromkeys([competitor.totalSteps for competitor in competitors])
        
        return list(stepsSet).index(self.totalSteps) + 1


    def getPlaceCurrentPerDay(self):

        """
        Get current place for user per day

        Parameters:
            Void
          
        Returns: 
            Integer - Place for user
        """

        today = timezone.now().date()

        dailyInstances = DailySteps.objects.filter(date=today)
        todaySteps = self.getStepsFromDay(today)
        stepsSet = OrderedDict.fromkeys([dailyInstanc.dailySteps for dailyInstance in dailyInstances])
        
        return list(stepsSet).index(todaySteps) + 1



    @staticmethod
    def getUsersInPlace(place):

        """
        Get users in specified position

        Parameters:
            place(Integer): Place to return
          
        Returns: 
            StepsCompetitor[]: List of competitors in place
        """

        index = place - 1
        competitors = StepsCompetitor.objects.only('totalSteps')
        stepsSet = OrderedDict.fromkeys([competitor.totalSteps for competitor in competitors])
        stepsOrdered = list(stepsSet)

        if index >= len(stepsOrdered):
            return []

        competitorsResult = StepsCompetitor.objects.filter(totalSteps=stepsOrdered[index])
        
        return competitorsResult


    @staticmethod
    def getUsersInPlacePerDay(place):

        """
        Get users in specified position per day

        Parameters:
            place(Integer): Place to return
          
        Returns: 
            StepsCompetitor[]: List of competitors in place
        """

        index = place - 1
        dailyInstances = DailySteps.objects.filter(date=today)
        stepsSet = OrderedDict.fromkeys([dailyInstanc.dailySteps for dailyInstance in dailyInstances])
        
        
        stepsOrdered = list(stepsSet)


        if index >= len(stepsOrdered):
            return []

        stepsInPlace = stepsOrdered[index]
        dailyStepsInPlace = dailyInstances.filter(dailySteps=stepsInPlace)

        competitorsResult = [dailyInstance.stepsCompetitor for dailyInstance in dailyStepsInPlace]
        
        return competitorsResult



    class Meta:
        ordering = ['-totalSteps']

        




