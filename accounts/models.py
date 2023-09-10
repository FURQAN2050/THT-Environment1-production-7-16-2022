import json
import datetime
import pytz
import math
import numpy as np
from PIL import Image
from io import BytesIO
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.utils import timezone
from django.conf import settings
from django.forms import ValidationError

from tools.mediaAbs import MediaAbs

# Create your models here.

def user_directory_path(instance, filename):

    """
    Returns path to save file model for image and video files
    file will be uploaded to 
    <media_folder>/<model>/user_<id>/<year>/<month>/<day>/
    """

    return '{0}/user_{1}/{2}/{3}/{4}/{5}'.format(
        type(instance).__name__,
        instance.added_by.id,
        timezone.now().year,
        timezone.now().month,
        timezone.now().day,
        str(instance.id) + "_"  + filename
        )

# WORKON: Make sure these processes are correct
# WORKON: Allow admin to select MAX_PARTICIPANTS for a team


class MediaAccount(MediaAbs):

    """
    Model that holds multimedia infomration

    Attributes:
        date(Datetime): Date when the value was created
        name(String): Name of the media
        thumbnail(ImageField): Thumbnail from media uploaded
        addedBy(ForeignKey): User that uploaded file
    """

    date = models.DateTimeField(default=timezone.now())
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to=user_directory_path, default=None)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):

        """
        Returns name of media as string
        """

        return self.name

    def save(self, *args, **kwargs):

        """
        Sets posted date for object
        """

        if not self.id:
            self.date = timezone.now()

        super(MediaAccount, self).save(*args, **kwargs)

        


    def saveThumbnailForImage(self, imageName, newName, size):

        """
        Provides a resized image of specified size from an image in a directory

        Parameters: 
            imageName(String) : Address to image to resize
            size(Integer[2]) : Size for image
          
        Returns: 
            Image: New image of size
        """

        name = newName + '.thumbnail.jpg'

        thumb_file = self.getThumbnailFromImage(imageName, name, size)

        self.thumbnail.save(name, thumb_file)

        return name


    def convertImageFieldToJPEG(self):

        if self.image_field:

            print("This is image_field if")

            name = self.name

            if not self.isImageJPG(self.image_field.read()):

                print("This is isimageJPG if")

                im = Image.open(self.image_field)
                im = im.convert('RGB')
                im.thumbnail([512, 512])

            else:

                im = Image.open(self.image_field)
                im.thumbnail([512, 512])
                
            output = BytesIO()
            im.save(output, format='JPEG')
            self.image_field.delete()
            self.image_field.save(name + ".jpg", output, save=False)


class ImageProfile(MediaAccount):

    """
    Model that holds an image

    Attributes:
        image(File): Image file
    """

    image_field = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """

        super(ImageProfile, self).save(*args, **kwargs)

class ImageBefore(MediaAccount):

    """
    Model that holds an image

    Attributes:
        image(File): Image file
    """

    image_field = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """

        super(ImageBefore, self).save(*args, **kwargs)

class ImageCurrent(MediaAccount):

    """
    Model that holds an image

    Attributes:
        image(File): Image file
    """

    image_field = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """

        super(ImageCurrent, self).save(*args, **kwargs)

# Extend User model

class User(AbstractUser):
    isDistrictManager = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default="US/Eastern")
    profilePicture = models.ForeignKey(ImageProfile, models.SET_NULL, blank=True, null=True)

# Model for teams

#WORKON: Add json functionality to team history points

class Teams(models.Model):

    COLORS = {
        'Green':'#5fba7d',
        'Red':'#6c2630',
        'Blue':'#16abfb',
        'Yellow':'#f7cd19',
        'Orange':'#ff6300',
        'Purple':'#ed00ff',
        'Pink':'#E91E63',
        'Brown':'#BB8D6F'
    }

    TEAMS = [
        ('Green', 'Green'), 
        ('Blue', 'Blue'), 
        ('Red', 'Red'),
        ('Yellow', 'Yellow'), 
        ('Orange', 'Orange'), 
        ('Purple', 'Purple'),
        ('Pink','Pink'),
        ('Brown','Brown')
        ]

    team = models.CharField(max_length=50)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, default=None)
    points = models.FloatField(default=0)
    historyPoints = models.TextField(null=True, default="[]")
    participants = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=10, null=True, default=None, choices=TEAMS)
    
    def __str__(self):
        if self.school != None:
            return self.team + " " + self.school.name
        else:
            return self.team + " no school"

    def get_points(self):
        """
        Returns points of all teachers associated with the team.
        Use instead of points variable.
        """
        teachers = self.teacher_set.all()
        teacher_points = [teacher.points for teacher in teachers]
        return sum(teacher_points)
    def get_teacher(self):
        """
        Returns points of all teachers associated with the team.
        Use instead of points variable.
        """
        teachers = self.teacher_set.all();
        teacher_username = [teacher.user.first_name+" "+teacher.user.last_name for teacher in teachers]
        teacher_points = [teacher.points for teacher in teachers];
        teacherAndPoints=[];
        for i in range(len(teacher_username)):
            teacherAndPoints.append( "Member: "+ str(teacher_username[i]) + " Points: "+ str(teacher_points[i]));
        return (teacherAndPoints);
    
    def get_num_participants(self):
        """
        Returns number of participants in the team
        Use instead of participants variable.
        """

        teachers = self.teacher_set.all()
        return len(teachers)



    class Meta:
        verbose_name_plural = "Teams"

# Returns available teams for a district

def availableTeams(mySchool):

    number_of_teams = len(mySchool.teams_set.all());

    availableTeams = Teams.objects.filter(school = mySchool)
    availableTeams = [i.team for i in availableTeams if i.get_num_participants() < math.ceil(mySchool.getNumParticipants() / number_of_teams)]
    return availableTeams

# Districts model


# Returns indvidual Team Points

def individualTeamPoints(mySchool):



    number_of_teams = len(mySchool.teams_set.all())
    availableTeams = Teams.objects.filter(school = mySchool)
    print(availableTeams);
    teamPoints = [team.get_points() for team in availableTeams]
    teamName = [team.team for team in availableTeams]
    teamColor = [team.color for team in availableTeams]
    teamAndPoints=[];
    for i in range(len(teamName)):
        teamAndPoints.append({"name":teamName[i],"points":teamPoints[i] ,"color": teamColor[i]});
    return teamAndPoints;
#WORKON: Add json functionality to district history points

class Districts(models.Model):
    district = models.CharField(max_length=100)
    emailDomain = models.CharField(db_index=True, max_length=100)
    points = models.FloatField(default=0)
    participants = models.IntegerField(default=0)
    historyPoints = models.TextField(null=True, default="[]")
    isIndependent = models.BooleanField(default=False)

    def __str__(self):
        return self.district

    def get_points(self):
        """
        Returns points of all teachers associated with the district.
        Use instead of points variable.
        """
        teachers = self.teacher_set.all()
        teacher_points = [teacher.points for teacher in teachers]
        return sum(teacher_points)

    class Meta:
        verbose_name_plural = "Districts"

# Create teams for each district when a district is created

def extraSaveForSchool(**kwargs):

    NUM_TEAMS = 3

    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
   
        for i in range(NUM_TEAMS):
            team = Teams(team = Teams.TEAMS[i][0], school = instance, points = 0, participants = 0, color = Teams.COLORS[Teams.TEAMS[i][0]])
            team.save()


class School(models.Model):

    name = models.CharField(max_length=100)
    district = models.ForeignKey('Districts', on_delete=models.CASCADE)

    @staticmethod
    def availableSchools(myDistrict):

        number_of_teams = len(myDistrict.school_set.all())

        availableSchools = School.objects.filter(district = myDistrict)
        availableSchools = [i.name for i in availableSchools]
        return availableSchools

    def getNumParticipants(self):
        return len(self.teacher_set.all())

    def __str__(self):
        return self.name

#WORKON: Need a privacy and terms and conditions statements for this data compliant with the HIPAA

class Subscriptions(models.Model):

    UNIT = [
        ('M', 'Months'),
        ('Y', 'Years')
    ]

    name = models.CharField(max_length=50, null=False)
    unit = models.CharField(max_length=1, choices=UNIT, default='M')
    length = models.IntegerField()
    price = models.FloatField()

    # Get length of a subscription
    def getEndDate(self, startDate):

        month = startDate.month
        year = startDate.year

        isLeap = False

        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            
            isLeap = True

        if self.unit == self.UNIT[0][0]:

            if month not in (2,4,6,9,11):
                days = 31

            elif month != 2:
                days = 30

            elif isLeap:
                days = 29
            
            else:
                days = 28

            return startDate + datetime.timedelta(days = days)

        elif self.unit == self.UNIT[1][0]:

            if isLeap:
                days = 366

            else:
                days = 365

            return startDate + datetime.timedelta(days = days)


    def __str__(self):
        return self.name + " $" + str(self.price)

    class Meta:
        verbose_name_plural = "Subscriptions"
   
class Teacher(models.Model):

    bmiConstant = 703

    SEDENTARY_CONST = 1.2
    LIGHT_ACTIVE_CONST = 1.375
    MODERATE_ACTIVE_CONST = 1.55
    ACTIVE_CONST = 1.725

    GENDER = [
        ('M','M'),
        ('F','F'),
    ]

    ACTIVITY_LEVEL = [
        ('S', 'Sedentary'),
        ('LA', 'Light Active'),
        ('MA', 'Moderately Active'),
        ('A', 'Active'),
    ]

    GOAL_OPTIONS = [
        ('F', 'Fat Loss'),
        ('M', 'Muscle Gain')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Teams', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    points = models.FloatField(default=0)
    district = models.ForeignKey('Districts', on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True)
    isIndividualAccount = models.BooleanField(default=None, null=True)
    processingSubscription = models.BooleanField(default=False, null=True)
    goodUntil = models.DateField(default=None, null=True)
    subscriptionType = models.ForeignKey('Subscriptions', on_delete=models.SET_NULL, blank=True, null=True, default=None)

    # Health related data

    gender = models.CharField(max_length=1, choices=GENDER, null=True, default=None)
    birthday = models.DateField(default=None, null=True)
    weight = models.FloatField(default=None, null=True)
    height = models.FloatField(default=None, null=True)
    sysBloodPressure = models.FloatField(default=None, null=True)
    diasBloodPressure = models.FloatField(default=None, null=True)
    cholesterol = models.FloatField(default=None, null=True)
    bmi = models.FloatField(default=None, null=True)
    waistSize = models.FloatField(default=None, null=True)
    isPrediabetic = models.BooleanField(default=None, null=True)
    isDiabetic = models.BooleanField(default=None, null=True)
    bmr = models.FloatField(default=None, null=True)
    activityLevel = models.CharField(max_length=2, default=None, null=True, choices=ACTIVITY_LEVEL)
    totalDailyEnergyExp = models.FloatField(default=None, null=True)
    energyConsumption = models.FloatField(default=None, null=True)
    goal = models.CharField(max_length=1, default=None, null=True, choices=GOAL_OPTIONS)
    proteins = models.FloatField(default=None, null=True)
    carbs = models.FloatField(default=None, null=True)
    fats = models.FloatField(default=None, null=True)
    isKeto = models.BooleanField(default=None, null=True)
    lastDiet = models.CharField(max_length=30, default=None, null=True)
    nutritionDetails = models.TextField(default=None, null=True)


    historyQuestions = models.TextField(null=True, default="[]")
    dailyPoints = models.TextField(null=True, default="[]")

    # Before and current pictures

    beforePicture = models.ForeignKey(ImageBefore, models.SET_NULL, blank=True, null=True)
    currentPicture = models.ForeignKey(ImageCurrent, models.SET_NULL, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Teachers"

    @property
    def get_birthday(self):
        return self.birthday.__format__("%Y-%m-%d")

    # Get points from a specific day

    def getPointsDay(self, date):
        
        jsonList = (json.loads(self.dailyPoints))
        dayPos = self.findDay(date)

        if dayPos == -1:
            
            return 0
        
        return jsonList[dayPos]["Points"]



    # Get status of a question

    def getQuestionStatus(self, questionID):

        jsonList = (json.loads(self.historyQuestions))

        questionPos = self.findQuestion(questionID)

        if questionPos == -1:
            return "None"
        
        else:
            question = next(question for question in jsonList if question["Question"] == questionID)
            
            if question["Answer"] == "yes":
                return "yes"

            else:
                return "no"

    def isSubscriptionGood(self):

        if self.district.isIndependent == False:

            return True

        if self.goodUntil == None:
            
            return False
        
        elif datetime.date.today() >= self.goodUntil and self.isIndividualAccount:

            return False

        else:

            return True

    def extendSubscription(self, date):

        self.goodUntil = date

        self.save()

    # Finds an object in a list that matches question and date and returns the position in the list.
    # If nothing is found it returns -1

    def findQuestion(self, questionID):

        jsonList = (json.loads(self.historyQuestions))

        pos = 0

        for jsonObject in jsonList:

            if jsonObject["Question"] == questionID:
                return pos

            pos += 1

        return -1

    # Finds a day in the daily points json string
    # If day does not exist, returns -1

    def findDay(self, date):

        jsonList = (json.loads(self.dailyPoints))

        pos = 0

        for jsonObject in jsonList:

            if jsonObject["Date"] == date:
                
                return pos

            pos += 1

        return -1

    # Adds the current question to the json array or updates an existing question.
    # Returns a string in json format with updated values

    def updateJSONQuestions(self, questionID, date, answer):

        jsonList = (json.loads(self.historyQuestions))

        questionPos = self.findQuestion(questionID)

        if questionPos == -1:

            jsonObject = {
                "Question" : questionID,
                "Date" : date,
                "Answer" : answer,
            }

            jsonList.append(jsonObject)

            # Sort the list

            jsonList = sorted(jsonList, key = lambda i : (i["Question"]))

        else:

            jsonList[questionPos]["Answer"] = answer

        jsonStringUpdated = json.dumps(jsonList)

        self.historyQuestions = jsonStringUpdated

        return jsonStringUpdated

    
    # Update daily points in json format for each user, team, and district

    def updateJSONDaily(self, date, points):

        jsonList = (json.loads(self.dailyPoints))

        dayPos = self.findDay(date)


        if dayPos == -1:

            jsonObject = {
                "Date" : date,
                "Points" : points,
            }

            jsonList.append(jsonObject)

            # Sort the list

            jsonList = sorted(jsonList, key = lambda i : (i["Date"]))

        else:

            jsonList[dayPos]["Points"] += points
        
        jsonStringUpdated = json.dumps(jsonList)

        self.dailyPoints = jsonStringUpdated

        return jsonStringUpdated


    # Adds points to the teacher
    # Points must be greater than 0

    def addPoints(self, points, date):

        self.points += points
        self.team.points += points
        self.district.points += points

        self.updateJSONDaily(date, points)

        self.save()
        self.team.save()
        self.district.save()


    # Reduces points from teacher
    # Points must not be more than teacher current points

    def reducePoints(self, points, date):

        self.points -= points
        self.team.points -= points
        self.district.points -= points

        self.updateJSONDaily(date, 0 - points)

        self.save()
        self.team.save()
        self.district.save()


    def calculateAge(self):

        return relativedelta(datetime.date.today(), self.birthday).years #(datetime.date.today() - self.birthday) / np.timedelta64(1,'Y')


    def calculateBmr(self):

        WEIGHT_CONSTANT = 10

        HEIGHT_CONSTANT = 6.25

        AGE_CONSTANT = -5

        AGE_OFFSET_MALE = 5

        AGE_OFFSET_FEMALE = -161

        KILOGRAMS_TO_POUNDS = 2.20462

        INCHES_TO_CM = 2.54

        # Pound to kg conversion

        weight_kg = self.weight / KILOGRAMS_TO_POUNDS

        # Inches to centimeters conversion

        height_cm = self.height * INCHES_TO_CM

        # Age calculate

        age = int(self.calculateAge())

        # Calculate bmr using Mifflin-St Joer Equation

        # If teacher is a female
        
        if self.gender == self.GENDER[1][0]:

            self.bmr = ( WEIGHT_CONSTANT * weight_kg + 
                    HEIGHT_CONSTANT * height_cm +
                    AGE_CONSTANT * age +
                    AGE_OFFSET_FEMALE )

        else:

            self.bmr = ( WEIGHT_CONSTANT * weight_kg + 
                    HEIGHT_CONSTANT * height_cm +
                    AGE_CONSTANT * age +
                    AGE_OFFSET_MALE )
        
    # Needs to be called after calculateBmr() and activityLevel is not null

    def calculateTotalDailyEnergyExp(self):

        switcher = {
            'S': self.SEDENTARY_CONST,
            'LA': self.LIGHT_ACTIVE_CONST,
            'MA': self.MODERATE_ACTIVE_CONST,
            'A': self.ACTIVE_CONST,
        }

        self.totalDailyEnergyExp = switcher[self.activityLevel] * self.bmr


    # Needs to be called after calculateTotalEnergyExp()

    def calculateConsumptionCal(self):

        FAT_LOSS_CONSTANT = -500

        MUSCLE_GAIN_CONSTANT =  250

        if self.goal == self.GOAL_OPTIONS[0][0]:

            self.energyConsumption = self.totalDailyEnergyExp + FAT_LOSS_CONSTANT

        if self.goal == self.GOAL_OPTIONS[1][0]:

            self.energyConsumption = self.totalDailyEnergyExp + MUSCLE_GAIN_CONSTANT
        

    # Calculates the amount of proteins that should be consumed in grams
    # Should be called after calculateTotalDailyEnergyExp()

    def calculateProtein(self):

        PROTEIN_FACTOR = .32
        
        PROTEIN_COEFFICIENT = 4

        self.proteins = (self.energyConsumption * PROTEIN_FACTOR) / PROTEIN_COEFFICIENT


    # Calculates the amount of carbs that should be consumed in grams
    # Should be called after calculateTotalDailyEnergyExp()

    def calculateCarbs(self):

        CARBS_FACTOR = .38
        
        CARBS_COEFFICIENT = 4

        self.carbs = (self.energyConsumption * CARBS_FACTOR) / CARBS_COEFFICIENT


    # Calculates the amount of fats that should be consumed in grams
    # Should be called after calculateTotalDailyEnergyExp()

    def calculateFats(self):

        FATS_FACTOR = .30
        
        FATS_COEFFICIENT = 9

        self.fats = (self.energyConsumption * FATS_FACTOR) / FATS_COEFFICIENT

    # Calculate age based on date of birth
    
    def age(dob):

        today = datetime.date.today()
        
        years = today.year - dob.year
        
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            years -= 1
        
        return years

class EmailTemplate(models.Model):
    template = models.TextField(null=True, default="")

    def getFirstTemplate():
        print('function called');
        first_row = EmailTemplate.objects.first()
        print(first_row.template);
        return first_row.template;


def image_delete_files(**kwargs):

    """
    Remove files from a Image model
    """

    image = kwargs.get('instance')

    if image.image_field:

        # Remove image

        image.image_field.delete(False)

        if image.thumbnail:

            # Remove thumbnail
            image.thumbnail.delete(False)
            


def extraDeleteForTeachers(**kwargs):
    
    instance = kwargs.get('instance')
    team = instance.team
    district = instance.district

    if instance.team != None:
        
        team.points -= instance.points
        team.participants -= 1
        district.participants -= 1
        district.points -= instance.points
        district.save()
        team.save()


def extraSaveForImages(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        
        instance.convertImageFieldToJPEG()
        
post_save.connect(extraSaveForSchool, School)
post_save.connect(extraSaveForImages, ImageProfile)
post_save.connect(extraSaveForImages, ImageBefore)
post_save.connect(extraSaveForImages, ImageCurrent)
pre_delete.connect(extraDeleteForTeachers, Teacher)
pre_delete.connect(image_delete_files, ImageProfile)
pre_delete.connect(image_delete_files, ImageBefore)
pre_delete.connect(image_delete_files, ImageCurrent)