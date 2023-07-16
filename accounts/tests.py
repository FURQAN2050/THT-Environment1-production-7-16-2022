from django.test import TestCase
from . import models

import datetime

# Create your tests here.

# Create a female teacher with traditional case variables

class TeacherTestCaseFemaleTraditional(TestCase):


    def setUp(self):

        self.user = models.User.objects.create_user(username='testuser', password='12345', isDistrictManager=False)

        self.districtO = models.Districts.objects.create(
            district = "TestDistrict",
            emailDomain = "test.com"
        )

        self.school = models.School.objects.create(
            name = 'TestSchool',
            district = self.districtO
        )

        self.team = models.Teams.objects.create(
            team = 'Green',
            color = 'Green',
            school = self.school
        )

        self.teacher = models.Teacher.objects.create(
            user = self.user,
            team = self.team,
            district = self.districtO,
            gender = models.Teacher.GENDER[1][0],
            birthday = datetime.datetime.now().date() - datetime.timedelta(days=8065),
            weight = 165,
            height = 72,
            sysBloodPressure = 120,
            diasBloodPressure = 70,
            cholesterol = 100,
            bmi = 20,
            waistSize = 35,
            isPrediabetic = False,
            isDiabetic = False,
            activityLevel ='LA',
            goal = 'F'
        )

        self.teacher.calculateBmr()
        self.teacher.calculateTotalDailyEnergyExp()
        self.teacher.calculateConsumptionCal()
        self.teacher.calculateProtein()
        self.teacher.calculateCarbs()
        self.teacher.calculateFats()


    def test_check_bmr(self):

        self.assertTrue((self.teacher.bmr - 1622) < 5 and
                        (self.teacher.bmr - 1622) > -5)



    def test_check_TDEE(self):

        self.assertTrue((self.teacher.totalDailyEnergyExp - 2230) < 5 and
                        (self.teacher.totalDailyEnergyExp - 2230) > -5)


    def test_check_EnergyConsumption(self):


        self.assertTrue((self.teacher.energyConsumption - 1730) < 5 and
                        (self.teacher.energyConsumption - 1730) > -5)


    
    def test_check_proteins(self):
        

        self.assertTrue((self.teacher.proteins - 138) < 5 and
                        (self.teacher.proteins - 138) > -5)


        
    def test_check_carbs(self):

        self.assertTrue((self.teacher.carbs - 164) < 5 and
                        (self.teacher.carbs - 164) > -5)



    def test_check_fats(self):

        self.assertTrue((self.teacher.fats - 58) < 5 and
                        (self.teacher.fats - 58) > -5)





# Create a female teacher with traditional case variables

class TeacherTestCaseMaleTraditional(TestCase):


    def setUp(self):

        self.user = models.User.objects.create_user(username='testuser', password='12345', isDistrictManager=False)

        self.districtO = models.Districts.objects.create(
            district = "TestDistrict",
            emailDomain = "test.com"
        )

        self.school = models.School.objects.create(
            name = 'TestSchool',
            district = self.districtO
        )

        self.team = models.Teams.objects.create(
            team = 'Green',
            color = 'Green',
            school = self.school
        )

        self.teacher = models.Teacher.objects.create(
            user = self.user,
            team = self.team,
            district = self.districtO,
            gender = models.Teacher.GENDER[0][1],
            birthday = datetime.datetime.now().date() - datetime.timedelta(days=8065),
            weight = 165,
            height = 72,
            sysBloodPressure = 120,
            diasBloodPressure = 70,
            cholesterol = 100,
            bmi = 20,
            waistSize = 35,
            isPrediabetic = False,
            isDiabetic = False,
            activityLevel ='LA',
            goal = 'M'
        )

        self.teacher.calculateBmr()
        self.teacher.calculateTotalDailyEnergyExp()
        self.teacher.calculateConsumptionCal()
        self.teacher.calculateProtein()
        self.teacher.calculateCarbs()
        self.teacher.calculateFats()


    def test_check_bmr(self):

        self.assertTrue((self.teacher.bmr - 1786) < 5 and
                        (self.teacher.bmr - 1786) > -5)



    def test_check_TDEE(self):

        self.assertTrue((self.teacher.totalDailyEnergyExp - 2455) < 5 and
                        (self.teacher.totalDailyEnergyExp - 2455) > -5 )



    def test_check_EnergyConsumption(self):

        self.assertTrue((self.teacher.energyConsumption - 2706) < 5 and
                        (self.teacher.energyConsumption - 2706) > -5)


    
    def test_check_proteins(self):

        self.assertTrue((self.teacher.proteins - 216.48) < 5 and
                        (self.teacher.proteins - 216.48) > -5)


        
    def test_check_carbs(self):

        self.assertTrue((self.teacher.carbs - 257.07) < 5 and
                        (self.teacher.carbs - 257.07) > -5)



    def test_check_fats(self):

        self.assertTrue((self.teacher.fats - 90.2) < 5 and
                        (self.teacher.fats - 90.2) > -5)




class TeamTestCaseTraditional(TestCase):

    def setUp(self):

        self.user = list()
        self.teacher = list()

        for i in range(10):
            self.user.append(models.User.objects.create_user(username='testuser'+str(i), password='12345', isDistrictManager=False))

        self.districtO = models.Districts.objects.create(
            district = "TestDistrict",
            emailDomain = "test.com"
        )

        self.school = models.School.objects.create(
            name = 'TestSchool',
            district = self.districtO
        )

        self.team = models.Teams.objects.create(
            team = 'Green',
            color = 'Green',
            school = self.school
        )

        
        for i in range(10):
            self.teacher.append(models.Teacher.objects.create(
                user = self.user[i],
                team = self.team,
                district = self.districtO,
                gender = models.Teacher.GENDER[0],
                birthday = datetime.date(1997, 5, 19),
                weight = 165,
                height = 72,
                sysBloodPressure = 120,
                diasBloodPressure = 70,
                cholesterol = 100,
                bmi = 20,
                waistSize = 35,
                isPrediabetic = False,
                isDiabetic = False,
                activityLevel ='LA',
                goal = 'F',
                points = i
            ))

    def test_check_points(self):
        self.assertTrue(self.team.get_points() == sum([i for i in range(10)]))



class DistrictTestCaseTraditional(TestCase):

    def setUp(self):

        self.user = list()
        self.teacher = list()

        for i in range(10):
            self.user.append(models.User.objects.create_user(username='testuser'+str(i), password='12345', isDistrictManager=False))

        self.districtO = models.Districts.objects.create(
            district = "TestDistrict",
            emailDomain = "test.com"
        )

        self.school = models.School.objects.create(
            name = 'TestSchool',
            district = self.districtO
        )

        self.team = models.Teams.objects.create(
            team = 'Green',
            color = 'Green',
            school = self.school
        )

        
        for i in range(10):
            self.teacher.append(models.Teacher.objects.create(
                user = self.user[i],
                team = self.team,
                district = self.districtO,
                gender = models.Teacher.GENDER[0],
                birthday = datetime.date(1997, 5, 19),
                weight = 165,
                height = 72,
                sysBloodPressure = 120,
                diasBloodPressure = 70,
                cholesterol = 100,
                bmi = 20,
                waistSize = 35,
                isPrediabetic = False,
                isDiabetic = False,
                activityLevel ='LA',
                goal = 'F',
                points = i
            ))

    def test_check_points(self):
        self.assertTrue(self.districtO.get_points() == sum([i for i in range(10)]))