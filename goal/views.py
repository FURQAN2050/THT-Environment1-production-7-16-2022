from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import html
from django.http import HttpResponseBadRequest

import json

from .models import MyGoal
from accounts.models import User

class GoalAPI(APIView):

    """
    API returns data about goals
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        try:
            if request.POST['action'] == 'getGoal':
                
                return Response(
                    self.getGoal(
                        user
                    )
                )

            elif request.POST['action'] == 'setGoal':         
                return Response(
                    self.setGoal(
                        request.POST['goal'],
                        user
                    )
                )

            else:
                return HttpResponseBadRequest()

        except:
            return HttpResponseBadRequest()


    def getGoal(self, user):

        """
        Gets user goal and returns empty if no goal has been set

        Parameters: 
            user(User): Current user
          
        Returns: 
            Dictionary: Dictionary with goal
        """

        goalInstance = MyGoal.objects.filter(user = user)
        goal = ""
        
        if len(goalInstance) > 0:
            goal = goalInstance[0].goal

        data = {
            "goal" : goal,
        }

        return data

    
    def setGoal(self, goal, user):

        """
        Sets user goal. Raises error if goal does not meet standards

        Parameters: 
            goal(String): Goal must be less than 200 characters
            user(User): Current user
          
        Returns: 
            Void
        """     

        if not MyGoal.setGoal(user, goal):
            raise Exception()

        return {}





        


