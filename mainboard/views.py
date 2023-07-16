from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts import models as accounts
from accounts import views as accounts_views
from . import models

import json
import datetime
import pytz

# Create your views here.

def responseNotFound(request, exception=None):

    return HttpResponseRedirect('/')

class MainBoardView(generic.CreateView):

    def get(self, request):

        user = request.user
        check = accounts_views.check_station(request)
        if check != None:
            return check

        # ******* TESTING REDIRECTION WITH DJANGO-CMS ******

        return redirect('/home/')

        # **************************************************


        profile_picture = (
            user.profilePicture.image_field.url 
            if user.profilePicture != None 
            else "None"
        )

        questions = models.Questions.objects.filter(date__exact=timezone.now().astimezone(pytz.timezone("US/Eastern")).date())
        dates = [question.date.strftime("%m/%d/%Y") for question in questions]

        data = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'profile_picture' : profile_picture,
            'data' : zip(questions, dates)
        }

        return render(request, 'index.html', data)


# API to get current and historic points

# WORKON:
# Create more validations
# Improve the way that date is passed to the server

class PointsData(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        user = request.user

        # Get points for user
        if(request.POST['action'] == 'currentPoints'):
            return Response(self.getCurrentPoints(user))

        # Update database with questions
        if(request.POST['action'] == 'questionAction'):

            if(len(models.Questions.objects.filter(id__exact=request.POST['question'])) == 1):
                
                return Response(
                    self.updateDatabaseQuestions(
                        user, 
                        request.POST['question'], 
                        request.POST['date'], 
                        request.POST['answer']
                        )
                        )

        # Get question status
        if(request.POST['action'] == 'questionStatus'):
            return Response({
                    "answer" : user.teacher.getQuestionStatus(request.POST['question']),
                    "today" : True if models.Questions.objects.filter(id__exact=request.POST['question'])[0].date == datetime.date.today() else False
                })

        # Get question status
        if(request.POST['action'] == 'dayPoints'):
            return Response({
                    "points" : user.teacher.getPointsDay(request.POST['date']),
                })
        
    def getCurrentPoints(self, user):

        myPoints = user.teacher.points
        teamPoints = user.teacher.team.get_points()
        districtPoints = user.teacher.district.get_points()

        data = {
            "myPoints" : myPoints,
            "teamPoints" : teamPoints,
            "districtPoints" : districtPoints,
        }

        return data

    
    # Updates database based on the question
    # Must be called before updateJSONQuestions

    def updateModelAnswer(self, user, questionID, date, answer):

        questionPos = user.teacher.findQuestion(questionID)

        # If question was not answered previously

        if questionPos == -1:

            if answer == "yes":

                user.teacher.points += 1
                user.teacher.team.points += 1
                user.teacher.district.points += 1

                # Add points to daily points record

                user.teacher.updateJSONDaily(date, 1)

            # If answer is "no" do nothing

        # If question was answered previously

        else:

            if answer == "yes":

                # If question's previous answer was no

                if user.teacher.getQuestionStatus(questionID) == "no":
                
                    user.teacher.points += 1
                    user.teacher.team.points += 1
                    user.teacher.district.points += 1

                    # Add points to daily points record
                    
                    user.teacher.updateJSONDaily(date, 1)

            else:

                # If teacher does not have less than 0 points

                if user.teacher.points > 0:

                    # If questions previous answer was yes

                    if user.teacher.getQuestionStatus(questionID) == "yes":


                
                        user.teacher.points -= 1
                        user.teacher.team.points -= 1
                        user.teacher.district.points -= 1

                        # Add points to daily points record
                        
                        user.teacher.updateJSONDaily(date, -1)
                



    # Update database with question answers

    def updateDatabaseQuestions(self, user, questionID, date, answer):

        self.updateModelAnswer(user, questionID, date, answer)

        # Update JSON records for users. Date is a string in format MM/DD/YYYY
        user.teacher.updateJSONQuestions(questionID, date, answer)

        user.teacher.save()
        user.teacher.team.save()
        user.teacher.district.save()

        data = {
            "success" : True,
        }
        
        return data

def redirect_view(request):
    return redirect('/pages/')