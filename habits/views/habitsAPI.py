from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import html
from django.http import HttpResponseBadRequest


import json


from ..models import Trainee, Question, QuestionInstance
from accounts.models import User


class HabitsAPI(APIView):

    """
    API returns data about habits
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if len(Trainee.objects.filter(user=user)) <= 0:

            if len(User.objects.filter(id=user.id)) <= 0:
            
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                self.__createTrainee__(user)


        try:
            if request.POST['action'] == 'requestQuestionOfDay':
                
                return Response(
                    self.requestQuestionOfDay(
                        user
                    )
                )

            elif request.POST['action'] == 'requestQuestion':         
                return Response(
                    self.requestQuestion(
                        request.POST['id']
                    )
                )

            elif request.POST['action'] == 'answerQuestion':
            
                return Response(
                    self.answerQuestion(
                        request.POST['id'],
                        request.POST['answer'],
                        user
                    )
                )

            elif request.POST['action'] == 'isQuestionAnswered':
            
                return Response(
                    self.isQuestionAnswered(
                        request.POST['id'],
                        user
                    )
                )

            elif request.POST['action'] == 'canAnswerQuestion':
            
                return Response(
                    self.canAnswerQuestion(
                        request.POST['id'],
                        user
                    )
                )

            elif request.POST['action'] == 'getQuestionAnswer':
            
                return Response(
                    self.getQuestionAnswer(
                        request.POST['id'],
                        user
                    )
                )

            elif request.POST['action'] == 'getPoints':
            
                return Response(
                    self.getPoints(
                        user
                    )
                )

            else:
                return HttpResponseBadRequest()

        except:
            return HttpResponseBadRequest()


    def __createTrainee__(self, user):

        """
        Creates a new Trainee object and associates a user with it.
        It saves the database

        Parameters: 
            user(User): Current user
          
        Returns: 
            Void
        """

        trainee = Trainee(user=user)
        trainee.save()

    def requestQuestionOfDay(self, user):

        """
        Gets the last order of questions from user that have yet to be answered. It 
        limits amount of questions that can be answered by one order per day.
        If no more questions, lists are returned empty.

        Parameters: 
            user(User): Current user
          
        Returns: 
            Dictionary: Dictionary with a list of questions
        """

        trainee = user.trainee
        questions = Question.getLastUnansweredOrder(trainee)

        data = {
            'questions' : [{
                    'id' : question.id,
                    'question' : question.question,
                    'answer' : self.getQuestionAnswer(question.id, user)['answer'] } 
                for question in questions
            ]
        }

        return data


    def requestQuestion(self, questionId):

        """
        Returns a question based on the questionId.

        Parameters: 
            questionId(Integer)
          
        Returns: 
            Dictionary: Dictionary with question requested
        """

        if not questionId.isnumeric():
            raise Exception()

        questions = Question.objects.filter(id = questionId)

        if len(questions) == 0:
            raise Exception()

        question = questions[0].question
        
        data = {
            'question' : question,
        }

        return data



    def answerQuestion(self, questionId, answer, user):

        """
        Answers a question and applies all corresponding points
        to trainee

        Parameters: 
            questionId(Integer)
            answer(Integer): 1 for True and 0 for False
            user(User)
          
        Returns: 
            Dictionary: Dictionary with success flag
        """

        if (int(answer) != 1 and int(answer) != 0) or not questionId.isnumeric():
            raise Exception()

        questions = Question.objects.filter(id = questionId)

        if len(questions) == 0:
            raise Exception()

        answer = int(answer)
        question = questions[0]
        answer = True if answer == 1 else False
        question.answerQuestion(answer, user)
    
        data = {
            'success' : True,
        }

        return data


    def isQuestionAnswered(self, questionId, user):

        """
        Checks if a question has been answered by a user

        Parameters: 
            questionId(Integer)
            user(User)
          
        Returns: 
            Dictionary
        """

        isAnswered = False
        questions = Question.objects.filter(id = questionId)

        if len(questions) == 0:
            raise Exception()

        question = questions[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)

        if len(questionInstance) > 0:
            isAnswered = True
    
        data = {
            'isAnswered' : isAnswered,
        }

        return data


    def canAnswerQuestion(self, questionId, user):

        """
        Checks if a user can answer a question based on order

        Parameters: 
            questionId(Integer)
            user(User)
          
        Returns: 
            Dictionary
        """

        canAnswer = False
        questions = Question.objects.filter(id = questionId)

        if len(questions) == 0:
            raise Exception()

        question = questions[0]
        questionsLastUnansweredOrder = Question.getLastUnansweredOrder(user.trainee)

        if len(questionsLastUnansweredOrder) == 0:
            canAnswer = True

        elif question.order <= questionsLastUnansweredOrder[0].order:
            canAnswer = True
    
        data = {
            'canAnswer' : canAnswer,
        }

        return data



    def getQuestionAnswer(self, questionId, user):

        """
        Gets questions answer from a trainee

        Parameters: 
            questionId(Integer)
            user(User)
          
        Returns: 
            Dictionary
        """

        questions = Question.objects.filter(id = questionId)

        if len(questions) == 0:
            raise Exception()

        question = questions[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)

        if len(questionInstance) == 0:
            answer = None

        else:
            answer = questionInstance[0].answer
    
        data = {
            'answer' : answer,
        }

        return data


    def getPoints(self, user):

        """
        Gets points from trainee

        Parameters: 
            user(User)
          
        Returns: 
            Dictionary
        """

        # trainee = Trainee.objects.filter(user = user)

        # if len(trainee) == 0:
        #     raise Exception()

        # trainee = trainee[0]
    
        data = {
            'points' : user.teacher.points,
        }

        return data



