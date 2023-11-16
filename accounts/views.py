import datetime
from decimal import Decimal

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, password_validation
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import render, redirect

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.dispatch import receiver


from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from .forms import UserCreationForm, SelectSchoolForm, FinishSignUpForm, EditMyProfileForm, HealthDataForm, SubscribeForm, MacronutrientsForm
from .tokens import account_activation_token

from . import models
from .models import User, Teacher, ImageProfile, ImageBefore, ImageCurrent
from .models import Teams as TeamsModel


# TEMPORARY REDIRECT TO LOGIN PAGE

def redirect_view(request):
    return redirect('/pages/')

def check_station(request):

    user = request.user

    if user.teacher.processingSubscription:
        return render(request, "subscriptionProcessing.html")

    if not user.teacher.isSubscriptionGood():
        return redirect('/accounts/subscribe/')

    if user.teacher.school == None:
        return redirect('/accounts/selectschool/')

    if user.teacher.team == None:
        return redirect('/accounts/finish/')

    if user.teacher.weight == 0.0:
        return redirect('/accounts/healthinfo')

    return None

# Create sign up view from user form

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('confirm')
    template_name = 'signup.html'

# Validate activation token link and redirect teacher to choose team

class Activate(generic.CreateView):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.teacher.district.participants += 1
            user.teacher.district.save()
            user.save()
            login(request, user)

            if not user.teacher.isSubscriptionGood():
                return redirect('subscribe')

            else:
                return redirect('selectschool')

        else:
            return HttpResponse('Activation link is invalid!')


class SelectSchool(generic.CreateView):

    def post(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.school != None:
            return redirect('/')

        form = SelectSchoolForm(request.POST)

        print(form)

        if form.is_valid():
            school = models.School.objects.filter(Q(name = form.cleaned_data['school']) & Q(district = user.teacher.district))[0]
            user.teacher.school = school
            user.teacher.save()
            return redirect('finish')

    def get(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.school != None:
            return redirect('/')

        # Ensure user is subscribed

        if not user.teacher.isSubscriptionGood():
                return redirect('subscribe')

        form = SelectSchoolForm()
        options = models.School.availableSchools(myDistrict = user.teacher.district)
        return render(request, 'selectschool.html', {'form': form, 'options': options})

# Manage user choosing team, render the form, and update database

class FinishSignUp(generic.CreateView):

    def post(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.team != None:
            return redirect('/')

            

        form = FinishSignUpForm(request.POST)

        if form.is_valid():
            team = TeamsModel.objects.filter(Q(team = form.cleaned_data['team']) & Q(school = user.teacher.school))[0]
            user.teacher.team = team
            user.teacher.save()
            team.participants += 1
            team.save()
            return redirect('healthinfo')

    def get(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.team != None:
            return redirect('/')

        if not user.teacher.isSubscriptionGood():
                return redirect('subscribe')

        form = FinishSignUpForm()
        options = models.availableTeams(mySchool = user.teacher.school)
        return render(request, 'finish.html', {'form': form, 'options': options})


class HealthDataEnter(generic.CreateView):

    def post(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.school == None:
            return redirect('/accounts/selectschool/')

        if user.teacher.team == None:
            return redirect('/accounts/finish/')

        form = HealthDataForm(request.POST)
        gender = HealthDataForm.GENDER_R
        diabetic = HealthDataForm.CLOSED_R
        prediabetic = HealthDataForm.CLOSED_R
        isKeto = HealthDataForm.CLOSED_R

        print(request.POST)

        print(form.errors)
    

        if form.is_valid():


            user.teacher.gender = models.Teacher.GENDER[0] if form.cleaned_data['gender'] == HealthDataForm.GENDER_R[0] else models.Teacher.GENDER[1]
            user.teacher.birthday = form.cleaned_data['birthday']
            user.teacher.weight = form.cleaned_data['weight']
            user.teacher.height = form.cleaned_data['height']
            user.teacher.sysBloodPressure = form.cleaned_data['sysBloodPressure']
            user.teacher.diasBloodPressure =form.cleaned_data['diasBloodPressure']
            user.teacher.cholesterol = form.cleaned_data['cholesterol']
            user.teacher.waistSize = form.cleaned_data['waistsize']
            user.teacher.isPrediabetic = True if form.cleaned_data['isPrediabetic'] == HealthDataForm.CLOSED_R[1] else False
            user.teacher.isDiabetic = True if form.cleaned_data['isDiabetic'] == HealthDataForm.CLOSED_R[1] else False
            user.teacher.isKeto = True if form.cleaned_data['isKeto'] == HealthDataForm.CLOSED_R[1] else False
            user.teacher.lastDiet = form.cleaned_data['lastDiet']
            user.teacher.nutritionDetails = form.cleaned_data['nutritionDetails']
            user.teacher.bmi = user.teacher.weight * Teacher.bmiConstant / user.teacher.height**2

            user.teacher.save()

            # WORKON Update Macros

            return redirect('macros')

        else:

            return render(request, 'healthinfo.html', {'form': form, 'gender': gender, 'isKeto': isKeto, 'diabetic': diabetic, 'prediabetic': prediabetic})

    def get(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        if user.teacher.school == None:
            return redirect('/accounts/selectschool/')

        # Ensure user only sees this page once and not later

        if user.teacher.team == None:
            return redirect('/accounts/finish/')

        # Ensure user only sees this page if it has not completed it before

        if user.teacher.weight != 0.0:
            print('in weight condition');
            return redirect('/')

        form = HealthDataForm()
        gender = HealthDataForm.GENDER_R
        diabetic = HealthDataForm.CLOSED_R
        prediabetic = HealthDataForm.CLOSED_R
        isKeto = HealthDataForm.CLOSED_R
        return render(request, 'healthinfo.html', {'form': form, 'gender': gender, 'isKeto': isKeto, 'diabetic': diabetic, 'prediabetic': prediabetic})

class MacronutrientsView(generic.CreateView):

    def post(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.school == None:
            return redirect('/accounts/selectschool/')

        if user.teacher.team == None:
            return redirect('/accounts/finish/')

        form = MacronutrientsForm(request.POST)

        if form.is_valid():


            user.teacher.activityLevel = form.cleaned_data['activityLevel']
            user.teacher.goal = form.cleaned_data['goal']

            user.teacher.calculateBmr()
            user.teacher.calculateTotalDailyEnergyExp()
            user.teacher.calculateConsumptionCal()
            user.teacher.calculateProtein()
            user.teacher.calculateCarbs()
            user.teacher.calculateFats()

            user.teacher.save()

            # WORKON Update Macros

            return redirect('/')

    def get(self, request):

        user = request.user

        # Ensure user is authenticated

        if not user.is_authenticated:
            return redirect('/accounts/login/')

        # Ensure user only sees this page once and not later

        if user.teacher.school == None:
            return redirect('/accounts/selectschool/')

        if user.teacher.team == None:
            return redirect('/accounts/finish/')

        # Ensure user only sees this page if it has not completed it before

        #if user.teacher.activityLevel != None:
        #    return redirect('/accounts/profile/edit')

        form = MacronutrientsForm()
        activity = Teacher.ACTIVITY_LEVEL
        goal = Teacher.GOAL_OPTIONS

        return render(request, 'macronutrients.html', {'form': form, 'goal': goal, 'activity': activity})


# API rendering information about available teams

class Teams(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        if request.POST['action'] == 'individualTeamPoints':
            self.indvidualTeamPoints=models.individualTeamPoints(mySchool = request.user.teacher.school);
            data={
                "teamPoints":self.indvidualTeamPoints,
                 "userTeam":request.user.teacher.team.team
            }
            return Response(data)


        else:
            # Return available teams

            self.myTeams = models.availableTeams(mySchool = request.user.teacher.school)

            data = {
                "teams": self.myTeams
            }

            return Response(data)


class Profile(generic.CreateView):

    TABS = ['Profile', 'HealthInfo', 'Macros']

    currentTab = TABS[0]

    def get(self, request, currentTab = currentTab):

        user = request.user
        check = check_station(request)

        if check != None:
            return check

        form = EditMyProfileForm()
        formHealth = HealthDataForm()
        formMacros = MacronutrientsForm()

        profile_picture = (
            user.profilePicture.image_field.url 
            if user.profilePicture != None 
            else "None"
        )

        image_before = (
            user.teacher.beforePicture.image_field.url 
            if user.teacher.beforePicture != None 
            else "None"
        )

        image_current = (
            user.teacher.currentPicture.image_field.url 
            if user.teacher.currentPicture != None 
            else "None"
        )

        args = {
            'form' : form,
            'formHealth' : formHealth,
            'formMacros' : formMacros,
            'username' : user.get_username(),
            'email' : user.email,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'profile_picture' : profile_picture,
            'district' : user.teacher.district.district,
            'team' : user.teacher.team.team,
            'color' : user.teacher.team.color,
            'gender' : HealthDataForm.GENDER_R[0] if user.teacher.gender == 'M' else HealthDataForm.GENDER_R[1],
            'genderOptions' : HealthDataForm.GENDER_R,
            'birthday' : user.teacher.get_birthday,
            'weight' : user.teacher.weight,
            'height' : user.teacher.height,
            'sysBloodPressure' : user.teacher.sysBloodPressure,
            'diasBloodPressure' : user.teacher.diasBloodPressure,
            'cholesterol' : user.teacher.cholesterol,
            'waistsize' : user.teacher.waistSize,
            'isPrediabetic' : HealthDataForm.CLOSED_R[1] if user.teacher.isPrediabetic == True else HealthDataForm.CLOSED_R[0],
            'isDiabetic' : HealthDataForm.CLOSED_R[1] if user.teacher.isDiabetic == True else HealthDataForm.CLOSED_R[0],
            'closedOptions' : HealthDataForm.CLOSED_R,
            'bmr' : user.teacher.bmr,
            'activityLevel' : user.teacher.activityLevel,
            'totalDailyEnergyExp' : user.teacher.totalDailyEnergyExp,
            'energyConsumption' : user.teacher.energyConsumption,
            'goal' : user.teacher.goal,
            'activityOptions' : user.teacher.ACTIVITY_LEVEL,
            'goalOptions' : user.teacher.GOAL_OPTIONS,
            'proteins' : user.teacher.proteins,
            'carbs' : user.teacher.carbs,
            'fats' : user.teacher.fats,
            'tabs': self.TABS,
            'currentTab' : currentTab,
            'isIndependent' : user.teacher.isIndividualAccount,
            'image_before' : image_before,
            'image_current' : image_current
            }
             
        return render(request, 'edit_profile.html', args)

    def post(self, request, currentTab = currentTab):

        if(request.POST["formtab"] == "profile"):

            form = EditMyProfileForm(request.POST, request.FILES)

            user = request.user

            if form.is_valid():

                if form.cleaned_data['profilePicture'] != None:

                    profilePic = ImageProfile()

                    profilePic.name = "profile.jpg"
                    profilePic.image_field = form.cleaned_data['profilePicture']
                    profilePic.added_by = user

                    profilePic.save()

                    user.profilePicture = profilePic
                    user.profilePicture.save()

                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']

                user.save()


            return redirect("edit_profile", currentTab=self.TABS[0])

        if(request.POST["formtab"] == "healthinfo"):

            form = HealthDataForm(request.POST, request.FILES)

            user = request.user

            print(form.errors)

            if form.is_valid():

                if form.cleaned_data['beforePicture'] != None:

                    imageBefore = ImageBefore()

                    imageBefore.name = "before.jpg"
                    imageBefore.image_field = form.cleaned_data['beforePicture']
                    imageBefore.added_by = user

                    imageBefore.save()

                    user.teacher.beforePicture = imageBefore
                    user.teacher.beforePicture.save()

                if form.cleaned_data['currentPicture'] != None:

                    imageCurrent = ImageCurrent()

                    imageCurrent.name = "after.jpg"
                    imageCurrent.image_field = form.cleaned_data['currentPicture']
                    imageCurrent.added_by = user

                    imageCurrent.save()

                    user.teacher.currentPicture = imageCurrent
                    user.teacher.currentPicture.save()


                user.teacher.gender = models.Teacher.GENDER[0][0] if form.cleaned_data['gender'] == HealthDataForm.GENDER_R[0] else models.Teacher.GENDER[1][0]
                user.teacher.birthday = form.cleaned_data['birthday']
                user.teacher.weight = form.cleaned_data['weight']
                user.teacher.height = form.cleaned_data['height']
                user.teacher.sysBloodPressure = form.cleaned_data['sysBloodPressure']
                user.teacher.diasBloodPressure =form.cleaned_data['diasBloodPressure']
                user.teacher.cholesterol = form.cleaned_data['cholesterol']
                user.teacher.waistSize = form.cleaned_data['waistsize']
                user.teacher.isPrediabetic = True if form.cleaned_data['isPrediabetic'] == HealthDataForm.CLOSED_R[1] else False
                user.teacher.isDiabetic = True if form.cleaned_data['isDiabetic'] == HealthDataForm.CLOSED_R[1] else False
                user.teacher.bmi = user.teacher.weight * Teacher.bmiConstant / user.teacher.height**2

                user.teacher.calculateBmr()
                user.teacher.calculateTotalDailyEnergyExp()
                user.teacher.calculateConsumptionCal()
                user.teacher.calculateProtein()
                user.teacher.calculateCarbs()
                user.teacher.calculateFats()

                user.teacher.save()

            return redirect("edit_profile", currentTab=self.TABS[1])

        if(request.POST["formtab"] == "macros"):

            form = MacronutrientsForm(request.POST)

            user = request.user

            if form.is_valid():

                user.teacher.activityLevel = form.cleaned_data['activityLevel']
                user.teacher.goal = form.cleaned_data['goal']

                user.teacher.calculateBmr()
                user.teacher.calculateTotalDailyEnergyExp()
                user.teacher.calculateConsumptionCal()
                user.teacher.calculateProtein()
                user.teacher.calculateCarbs()
                user.teacher.calculateFats()

                user.teacher.save()

            return redirect("edit_profile", currentTab=self.TABS[2])

            


class Password(generic.CreateView):

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password_change.html', {'form' : form})

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile/edit')

        return render(request, 'password_change.html', {'form' : form})



class SubscribeView(generic.CreateView):

    def get(self, request):

        user = request.user

        # Ensure user only sees this page if they need to subscribe or renew subscription

        if user.teacher.isSubscriptionGood():
            return redirect('/accounts/profile/edit/')

        form = SubscribeForm()
        options = models.Subscriptions.objects.all()

        if user.teacher.subscriptionType != None:

            welcome = "It seems like your subscription is expired. Renew your subscription here!"

        else:

            welcome = ""

        return render(request, 'subscribe.html', {'form': form, 'options': options, 'welcome': welcome,})

    def post(self, request):

        form = SubscribeForm(request.POST)
        
        if form.is_valid():

            cleaned_data = form.cleaned_data
 
            request.session['order'] = request.POST['order']

            return redirect('process_payment')


# Processes payment for individual teachers using Paypal
    
class ProcessPayment(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        
        order = models.Subscriptions.objects.get(id=request.POST["OrderID"])
        host = request.get_host()
    
        paypal_dict = {
            'cmd': "_xclick-subscriptions",
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'a3': '%.2f' % order.price, # price
            'p3': order.length, # unit number
            't3': order.unit, # duration unit
            'src': '1', # payments recur
            'sra': '1', # reattempt on payment error
            'no_note': '1', 
            'item_name': order.name,
            'custom': user.id,
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,
                                            reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,
                                            reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host,
                                                reverse('payment_cancelled')),
        }
    
        form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
        return Response({'form': form.render()})


class LoginUser(LoginView):
    template_name = 'login.html'  # your template


@csrf_exempt
def payment_done(request):
    return render(request, 'subscriptionTimeInfo.html')
 

# Add a note here
@csrf_exempt
def payment_cancelled(request):
    return render(request, 'paymentCancelled.html')