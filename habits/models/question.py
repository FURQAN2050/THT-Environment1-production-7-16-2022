from django.db import models
from django.utils import timezone

from .questionInstance import QuestionInstance

import datetime

class Question(models.Model):

    """
    Model to represent a question for teachers

    Attributes:

        question(String)
        order(Integer): Defines the day the question will appear
        points(Integer): How many points this question gives teachers

    """

    question = models.TextField()
    order = models.IntegerField(default=1)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question

    def __createQuestionInstance__(self, answer, trainee):

        """
        Creates an instance for the current Question

        Parameters: 
            answer(Boolean)
            trainee(Trainee)
          
        Returns: 
            QuestionsInstance: Created instance (already saved to database)
        """

        questionInstance = QuestionInstance()
        questionInstance.trainee = trainee
        questionInstance.dateCreated = timezone.now()
        questionInstance.question = self
        questionInstance.setAnswer(answer)

        return questionInstance

    def answerQuestion(self, answer, user):

        """
        Creates Question Instance if not already created, and inserts answer
        
        Parameters:
            answer(Boolean)
            questionId(Integer)

        Returns:
            Void

        """

        points = 0
        trainee = user.trainee
            
        questionInstance = QuestionInstance.objects.filter(question = self, trainee = trainee)

        if len(questionInstance) == 0:
            questionInstance = self.__createQuestionInstance__(answer = answer, trainee = trainee)

        else:
            questionInstance = questionInstance[0]

            # If Trainee had answered question with true previously, offset points variable
            if questionInstance.answer == True:
                points -= self.points

        if answer == True:
            points += self.points
        
        trainee.points += points
        user.teacher.addPoints(points, timezone.now().date().strftime("%m/%d/%Y"))
        questionInstance.answer = answer
        questionInstance.save()
        trainee.save()

    
    @staticmethod
    def getLastUnansweredOrder(trainee):

        """
        Gets the last order of questions that have yet to be answered. It 
        limits amount of questions that can be answered by one order per day
        
        Parameters:
            user(User)

        Returns:
            Questions[0...*]

        """

        questionInstances = QuestionInstance.objects.filter(trainee = trainee).order_by('-question__order')

        if len(questionInstances) == 0:
            questions = Question.objects.all().order_by('order')
            minimum_order = min(questions, key=lambda x: x.order).order
            questions = [question for question in questions if question.order == minimum_order]

        
        else:
            lastOrder = questionInstances[0].question.order
            questions = Question.objects.filter(order = lastOrder)

            questionInstances = [questionInstance for questionInstance in questionInstances if questionInstance.question.order == lastOrder]

            # Calculate how long ago the last questions were answered

            # Get latest date
            maxDate = max(questionInstances, key=lambda x: x.dateCreated).dateCreated

            # Check if latest date was today
            dateDiff = timezone.now().date() - questionInstances[0].dateCreated.date()

            if len(questions) <= len(questionInstances) and dateDiff >= datetime.timedelta(1):
                questions = Question.objects.filter(order__gt = lastOrder).order_by('order')
                
                if len(questions) > 0:
                    minimum_order = min(questions, key=lambda x: x.order).order
                    questions = [question for question in questions if question.order == minimum_order]

        return list(questions)
            
