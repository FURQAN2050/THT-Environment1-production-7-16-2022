from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import datetime

from . import models
from accounts.models import User, Teacher, Teams, Districts

# Create your tests here.

USERNAME = 'lsavast'
PASSWORD = 'Leon2205'

class QuestionsResponseTraditionalTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD, isDistrictManager=False)
        
        self.districtO = Districts.objects.create(
            district = "TestDistrict",
            emailDomain = "test.com"
        )

        self.team = Teams.objects.create(
            team = 'Green',
            district = self.districtO,
            color = 'Green'
        )

        self.teacher = Teacher.objects.create(
            user = self.user,
            team = self.team,
            district = self.districtO,
            gender = Teacher.GENDER[1],
            birthday = datetime.date(1987, 5, 19),
            weight = 155.76,
            height = 69.68,
            sysBloodPressure = 120,
            diasBloodPressure = 70,
            cholesterol = 100,
            bmi = 20,
            waistSize = 35,
            isPrediabetic = False,
            isDiabetic = False,
            activityLevel = Teacher.MODERATE_ACTIVE_CONST,
            goal = Teacher.GOAL_OPTIONS[0]
        )

        self.client = APIClient()
        self.client.login(username=USERNAME, password=PASSWORD)

        for i in range(1, 11):
            
            question = models.Questions()

            question.id = i
            
            question.question="Test question " + str(i)
            
            question.date = datetime.datetime.today().strftime("%Y-%m-%d")
            
            question.save()

            print("Question id: ", question.id)

    def test_unanswered_question_response_yes(self):

        question = models.Questions.objects.filter(id=1)[0]

        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 1) < 0.1 and (teacher.points - 1) > -0.1)

    def test_answered_yes_question_response_yes(self):

        question = models.Questions.objects.filter(id=1)[0]

        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})
        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 1) < 0.1 and (teacher.points - 1) > -0.1)


    def test_answered_yes_question_response_no(self):

        question = models.Questions.objects.filter(id=1)[0]

        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})
        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"no"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 0) < 0.1 and (teacher.points - 0) > -0.1)

    def test_answered_no_question_response_no(self):

        question = models.Questions.objects.filter(id=1)[0]

        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"no"})
        response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"no"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 0) < 0.1 and (teacher.points - 0) > -0.1)

    def test_answered_no_yes_many_times_question_final_response_no(self):

        question = models.Questions.objects.filter(id=1)[0]

        for i in range(10):
            response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})
            response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"no"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 0) < 0.1 and (teacher.points - 0) > -0.1)

    def test_multiple_questions_final_answer_no(self):

        for i in range(1,11):

            question = models.Questions.objects.filter(id=i)[0]
            
            response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})
        
        for i in range(1, 11):

            question = models.Questions.objects.filter(id=i)[0]

            response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"no"})

        for i in range(1, 5):

            question = models.Questions.objects.filter(id=i)[0]

            response = self.client.post('/board/api/data/', {'action':'questionAction', 'question':question.id, 'date':question.date.strftime("%Y-%m-%d"), 'answer':"yes"})

        user = User.objects.get(username='lsavast')
        teacher = user.teacher

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((teacher.points - 4) < 0.1 and (teacher.points - 4) > -0.1)




        