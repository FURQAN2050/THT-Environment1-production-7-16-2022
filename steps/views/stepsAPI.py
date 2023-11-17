from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import html
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.utils.dateparse import parse_datetime

import json
import datetime

from tools.utils import daterange

from ..models import DailySteps, StepsCompetitor
from accounts.models import User

class StepsAPI(APIView):

    """
    API returns data about goals
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if len(StepsCompetitor.objects.filter(user=user)) <= 0:

            if len(User.objects.filter(id=user.id)) <= 0:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                self.__createStepsCompetitor__(user)

        try:
            if request.POST['action'] == 'getTotalSteps':
                
                return Response(
                    self.getTotalSteps(
                        user
                    )
                )

            elif request.POST['action'] == 'getStepsDate':
                date = self.__convertStringToDate__(request.POST['date'])
                return Response(
                    self.getStepsDate(
                        user,
                        date
                    )
                )

            elif request.POST['action'] == 'getStepsDateRange':
                dateStart = self.__convertStringToDate__(request.POST['dateStart'])
                dateEnd = self.__convertStringToDate__(request.POST['dateEnd'])
                return Response(
                    self.getStepsDateRange(
                        user,
                        dateStart,
                        dateEnd,
                    )
                )

            elif request.POST['action'] == 'recordStepsToday':
                return Response(
                    self.recordStepsToday(
                        user,
                        request.POST['steps']
                    )
                )

            elif request.POST['action'] == 'recordSteps':
                date = self.__convertStringToDate__(request.POST['date'])
                return Response(
                    self.recordSteps(
                        user,
                        request.POST['steps'],
                        date
                    )
                )

            elif request.POST['action'] == 'getPlaceCurrent':
                return Response(
                    self.getPlaceCurrent(
                        user
                    )
                )

            elif request.POST['action'] == 'getPlaceCurrentPerDay':
                return Response(
                    self.getPlaceCurrentPerDay(
                        user
                    )
                )

            elif request.POST['action'] == 'getUserInPlace':
                return Response(
                    self.getUsersInPlace(
                        user,
                        request.POST['place'],
                    )
                )

            elif request.POST['action'] == 'getUserInPlacePerDay':
                return Response(
                    self.getUsersInPlacePerDay(
                        user,
                        request.POST['place'],
                    )
                )

            else:
                return HttpResponseBadRequest()

        except:
            return HttpResponseBadRequest()


    def __createStepsCompetitor__(self, user):

        """
        Creates a new StepsCompetitor object and associates a user with it.
        It saves the database

        Parameters: 
            user(User): Current user
        
        Returns: 
            Void
        """

        stepsCompetitor = StepsCompetitor(user=user)
        stepsCompetitor.save()


    def __convertStringToDate__(self, dateString):

        """
        Converts a date in string format to Date object

        Parameters: 
            dateString(String): Date to convert in format yyyy/mm/dd
        
        Returns: 
            Date
        """

        date = datetime.datetime.strptime(dateString, "%Y-%m-%d").date()

        return date
    
    def __convertISOStringToDate__(self, dateString):

        """
        Converts a date in string format to Date object

        Parameters: 
            dateString(String): Date to convert in format yyyy/mm/dd
        
        Returns: 
            Date
        """

            # date = datetime.datetime.strptime(dateString, "%Y-%m-%d").date()
        date= parse_datetime(dateString)

        return date


    def getTotalSteps(self, user):

        """
        Gets total steps from current user

        Parameters: 
            user(User): Current user
        
        Returns: 
            Integer: Number of steps
        """

        stepsCompetitor = user.stepscompetitor
        totalSteps = stepsCompetitor.getTotalSteps()

        data = {
            'totalSteps' : totalSteps,
        }
        
        return data

    
    def getStepsDate(self, user, date):

        """
        Gets total steps from current user from specific date

        Parameters: 
            user(User): Current user
            date(Date)
        
        Returns: 
            Integer: Number of steps
        """

        stepsCompetitor = user.stepscompetitor
        stepsFromDay = stepsCompetitor.getStepsFromDay(date)

        data = {
            'stepsFromDay' : stepsFromDay,
        }

        return data
        

    def getStepsDateRange(self, user, dateStart, dateEnd):

        """
        Gets total steps from current user from specific date range

        Parameters: 
            user(User): Current user
            dateStart(Date)
            dateEnd(Date)
        
        Returns: 
            Dictionary: List with number of steps per day
        """

        stepsCompetitor = user.stepscompetitor
        stepsDays = {}

        for date in daterange(dateStart, dateEnd):
            stepsFromDay = stepsCompetitor.getStepsFromDay(date)
            stepsDays[str(date)] = stepsFromDay

        data = {
            'stepsDateRange' : stepsDays,
        }

        return data

    
    def recordStepsToday(self, user, steps):

        """
        Record steps for today

        Parameters: 
            user(User): Current user
            steps(Integer): Number of steps
        
        Returns: 
            Void
        """

        if not steps.isnumeric():
            raise Exception()

        date = timezone.now().date()
        stepsCompetitor = user.stepscompetitor
        stepsCompetitor.recordSteps(steps, date,user)

    
    def recordSteps(self, user, steps, date):

        """
        Record steps on a specific date

        Parameters: 
            user(User): Current user
            steps(Integer): Number of steps
            date(Date): Date to record steps to
        
        Returns: 
            Void
        """

        if not steps.isnumeric():
            raise Exception()

        stepsCompetitor = user.stepscompetitor
        stepsCompetitor.recordSteps(steps, date)



    def getPlaceCurrent(self, user):

        """
        Get place of current user

        Parameters: 
            user(User): Current user
        
        Returns: 
            Integer
        """

        stepsCompetitor = user.stepscompetitor
        
        data = { 
            "place" : stepsCompetitor.getPlaceCurrent(),
            }

        return data


    def getPlaceCurrentPerDay(self, user):

        """
        Get place of current user per day

        Parameters: 
            user(User): Current user
        
        Returns: 
            Integer
        """

        stepsCompetitor = user.stepscompetitor
        
        data = { 
            "place" : stepsCompetitor.getPlaceCurrentPerDay(),
            }

        return data



    def getUsersInPlace(self, user, place):

        """
        Get users in specified position

        Parameters:
            place(Integer): Place to return
          
        Returns: 
            Dictionary: With username and steps
        """

        if not place.isnumeric():
            raise Exception()

        stepsCompetitor = user.stepscompetitor.getUsersInPlace(int(place))
        
        data = { 
            "username" : [competitor.user.username for competitor in stepsCompetitor],
            "steps" : [competitor.totalSteps for competitor in stepsCompetitor]
            }

        return data

    
    def getUsersInPlacePerDay(self, user, place):

        """
        Get users in specified position per day

        Parameters:
            place(Integer): Place to return
          
        Returns: 
            Dictionary: With username and steps
        """

        if not place.isnumeric():
            raise Exception()

        stepsCompetitor = user.stepscompetitor.getUsersInPlacePerDay(int(place))
        
        data = { 
            "username" : [competitor.user.username for competitor in stepsCompetitor],
            "steps" : [competitor.totalSteps for competitor in stepsCompetitor]
            }

        return data