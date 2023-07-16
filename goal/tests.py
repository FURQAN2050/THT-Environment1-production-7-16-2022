from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import datetime

from .models import MyGoal
from accounts.models import User, Teacher, Teams, Districts

# Create your tests here.

USERNAME = 'lsavast'
PASSWORD = 'Leon1111'

class GoalAPITraditionalTestCase(TestCase):

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

    def test_get_goal_existing_goal(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        response = self.client.post('/goal/api/data/', {'action':'getGoal'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['goal'], "test")


    def test_get_goal_non_existing_goal(self):

        response = self.client.post('/goal/api/data/', {'action':'getGoal'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['goal'], "")


    def test_set_goal_non_existing_goal(self):

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': 'test'})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goalInstance[0].goal, "test")


    def test_set_goal_existing_goal(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': 'testChange'})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goalInstance[0].goal, "testChange")


    def test_set_goal_existing_goal(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': 'testChange'})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goalInstance[0].goal, "testChange")


    def test_set_goal_existing_goal_to_empty(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': ''})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goalInstance[0].goal, "")


    def test_set_goal_existing_goal_too_large(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        goalSet = "a" * 250

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': goalSet})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(goalInstance[0].goal, "test")


    def test_set_goal_existing_goal_boundary_length(self):

        goal = MyGoal(user = self.user, goal = "test")
        goal.save()

        goalSet = "a" * MyGoal.MAX_GOAL_LEN

        response = self.client.post('/goal/api/data/', {'action':'setGoal', 'goal': goalSet})

        goalInstance = MyGoal.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(goalInstance[0].goal, goalSet)
