from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import datetime

from django.db import models

from .models import DailySteps, StepsCompetitor
from accounts.models import User, Teacher, Teams, Districts

# Create your tests here.

USERNAME = 'lsavast'
PASSWORD = 'Leon1111'

def districtFactory(districtName, emailDomain):

    district = Districts.objects.create(
            district = districtName,
            emailDomain = emailDomain
        )

    return district


def teamFactory(color, district):

    team = Teams.objects.create(
            team = color,
            district = district,
            color = color
        )

    return team


def teacherFactory(user, team, district, 
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
            goal = Teacher.GOAL_OPTIONS[0]):

    teacher = Teacher.objects.create(
            user = user,
            team = team,
            district = district,
            gender = gender,
            birthday = birthday,
            weight = weight,
            height = height,
            sysBloodPressure = sysBloodPressure,
            diasBloodPressure = diasBloodPressure,
            cholesterol = cholesterol,
            bmi = bmi,
            waistSize = waistSize,
            isPrediabetic = isPrediabetic,
            isDiabetic = isDiabetic,
            activityLevel = activityLevel,
            goal = goal
        )

    return teacher

class StepsAPITraditionalTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD, isDistrictManager=False)
        self.districtO = districtFactory('TestDistrict', 'test.com')
        self.team = teamFactory('Green', self.districtO)
        self.teacher = teacherFactory(self.user, self.team, self.districtO)
        self.client = APIClient()
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_record_steps_today(self):

        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':0})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 0)



    def test_record_many_steps_today(self):

        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':10000})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 10000)



    def test_record_steps_today_many_times(self):

        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':10000})
        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':20000})
        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':30000})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 30000)


    def test_record_steps_0(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':0, 'date':'2020-04-21'})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 0)


    def test_record_steps_many(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-05-21'})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 10000)


    def test_record_steps_many_days(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':20000, 'date':'2020-04-22'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-24'})

        totalSteps = 0

        days = DailySteps.objects.filter(stepsCompetitor = self.user.stepscompetitor)
        
        for day in days:
            totalSteps += day.dailySteps

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(totalSteps, 40000)


    def test_get_total_steps_0(self):

        response = self.client.post('/steps/api/data/', {'action':'getTotalSteps'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['totalSteps'], 0)


    def test_get_total_steps_many(self):

        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':10000})
        response = self.client.post('/steps/api/data/', {'action':'getTotalSteps'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['totalSteps'], 10000)


    def test_get_total_steps_many_days(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':20000, 'date':'2020-04-22'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-23'})
        response = self.client.post('/steps/api/data/', {'action':'getTotalSteps'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['totalSteps'], 40000)


    def test_get_steps_date_0(self):

        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-21'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 0)


    def test_get_steps_date_many(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-21'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 10000)


    def test_get_steps_date_many_days(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-21'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 10000)

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':20000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-21'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 20000)

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':30000, 'date':'2020-04-23'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':35000, 'date':'2020-04-24'})
        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':37000, 'date':'2020-04-25'})
        
        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-23'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 30000)

        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-24'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 35000)

        response = self.client.post('/steps/api/data/', {'action':'getStepsDate', 'date':'2020-04-25'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stepsFromDay'], 37000)


    def test_get_place_current_only_user(self):

        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':10000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 1)


    def test_get_place_current_multiple_users_last(self):

        for i in range(0,2):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordSteps', 'steps':(2000 + i*1000), 'date':'2020-04-21'})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':1000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 3)


    def test_get_place_current_multiple_users_middle(self):

        for i in range(0,2):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordSteps', 'steps':(2000 + i*1000), 'date':'2020-04-21'})


        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':2500})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 2)



    def test_get_place_current_multiple_users_middle(self):

        for i in range(0,2):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(2000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':2500, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 2)


        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':2000})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 1)


    def test_get_place_current_multiple_users_ties_middle(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(2000 + (i%3)*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':3000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 2)


        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':2000})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 1)



    def test_get_place_current_multiple_users_middle(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 4)


        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':2000})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 2)

    
    def test_get_place_current_multiple_users_middle(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 4)


        response = self.client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':2000})
        response = self.client.post('/steps/api/data/', {'action':'getPlaceCurrent'})


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 2)


    def test_get_user_in_place_routine_many(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getUserInPlace', 'place': 4})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['username']), 2)
        self.assertTrue('lsavast' in response.data['username'] and 'user4' in response.data['username'])
        self.assertTrue(5000 in response.data['steps'])


    def test_get_user_in_place_routine_many_first(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getUserInPlace', 'place': 8})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['username']), 1)
        self.assertTrue('user0' in response.data['username'])
        self.assertTrue(1000 in response.data['steps'])


    def test_get_user_in_place_routine_many_last(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getUserInPlace', 'place': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['username']), 1)
        self.assertTrue('user7' in response.data['username'])
        self.assertTrue(8000 in response.data['steps'])


    def test_get_user_in_place_routine_many_outofbounds(self):

        for i in range(0,8):
            user = User.objects.create_user(username='user'+str(i), password=PASSWORD, isDistrictManager=False)
            teacher = teacherFactory(user, self.team, self.districtO)
            client = APIClient()
            client.login(username='user'+str(i), password=PASSWORD)
            response = client.post('/steps/api/data/', {'action':'recordStepsToday', 'steps':(1000 + i*1000)})


        response = self.client.post('/steps/api/data/', {'action':'recordSteps', 'steps':5000, 'date':'2020-04-21'})
        response = self.client.post('/steps/api/data/', {'action':'getUserInPlace', 'place': 9})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['username']), 0)