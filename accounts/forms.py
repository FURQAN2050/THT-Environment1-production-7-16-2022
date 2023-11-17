from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from .tokens import account_activation_token
from .models import User
from .models import Districts
from .models import Teacher
from .models import Subscriptions
from .models import School
from .models import EmailTemplate
import datetime

api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# WORKON: Make sure these processes are correct
# WORKON: Add extra questions to form
# WORKON: If on keto diet, do not calculate macros yet

# Sign up form extended. Sends confirmation email and creates a teacher

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    personalemail=forms.EmailField(required=True)
    state=forms.CharField(max_length=100)
    teacherschool=forms.CharField(max_length=100)
    gradeteach=forms.CharField(max_length=100)
    teacherprofessionlength=forms.CharField(max_length=100)
    gender=forms.CharField(max_length=100);

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "personalemail",
            "state",
            "teacherschool",
            "gradeteach",
            "teacherprofessionlength",
            "gender"
        )

    def save(self, commit=True):
        print('in save function');
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.personalemail = self.cleaned_data['personalemail']
        user.state = self.cleaned_data['state']
        user.teacherschool = self.cleaned_data['teacherschool']
        user.gradeteach = self.cleaned_data['gradeteach']
        user.teacherprofessionlength = self.cleaned_data['teacherprofessionlength']

        user.is_active = False
        print(user.email);

        if commit:
            user.save()

            # Send confirmation email to user to activate account

            mail_subject = "Activate your Healthy Teacher Account"

            emailTemplate=EmailTemplate.getFirstTemplate();
            if(emailTemplate):
                print('email template found')
                hyperlink='http://'+settings.SITE_HOST+'/accounts/activate/'+urlsafe_base64_encode(force_bytes(user.pk))+'/'+account_activation_token.make_token(user)+'/'
                messagehtml='<!DOCTYPE html> \n <html lang="en"> \n <head></head> \n <body>'+ emailTemplate +'\n</body> \n'
                messagehtml=messagehtml.replace('{{ user.first_name }}',user.first_name);
                messagehtml=messagehtml.replace('{{ hyperlink }}',hyperlink);
                print(messagehtml);
            else:
                messagehtml = render_to_string(EmailTemplate.getFirstTemplate(), {
                    'user': user,
                    'domain': settings.SITE_HOST,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
            messageplain = render_to_string('acc_active_email_plain.html', {
                    'user': user,
                    'domain': settings.SITE_HOST,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })

            to_email = self.cleaned_data['email']

            email = EmailMultiAlternatives(
                mail_subject, messageplain, to=[to_email]
            )
            email.attach_alternative(messagehtml, "text/html")

            email.send()

        if user.isDistrictManager == False:
            userGender=self.cleaned_data['gender']

            
            if Districts.objects.filter(emailDomain__icontains=self.cleaned_data['email'].split('@')[1]).exists():
            
                teacher = Teacher(user = user, 
                                  district = Districts.objects.filter(emailDomain__icontains=self.cleaned_data['email'].split('@')[1])[0],
                                  gender=userGender,
                                  weight=0,
                                  height=0,
                                  sysBloodPressure=0,
                                  diasBloodPressure=0,
                                  cholesterol=0,
                                  waistSize=0,
                                  birthday = datetime.datetime.now().date() - datetime.timedelta(days=8065),
                                  isPrediabetic = False,
                                  isDiabetic = False,
                                  );
                teacher.save()

            else:

                teacherDistrict = self.createIndependentDistrict(self.cleaned_data['email'])
                school = School(name="Other", district=teacherDistrict)
                school.save()
                teacher = Teacher(user = user, 
                                  district = teacherDistrict,
                                  gender=userGender,
                                  weight=0,
                                  height=0,
                                  cholesterol=0,
                                  sysBloodPressure=0,
                                  diasBloodPressure=0,
                                  waistSize=0,
                                  birthday = datetime.datetime.now().date() - datetime.timedelta(days=8065),
                                  isPrediabetic = False,
                                  isDiabetic = False,
                                  );
                teacher.save()


            
            if teacher.district.isIndependent == True:

                teacher.isIndividualAccount = True

            else:

                teacher.isIndividualAccount = False

            teacher.save()
            
        self.addSignupUserToMailChimp(user);    
        return user

    def createIndependentDistrict(self, email):

        domain = self.cleaned_data['email'].split('@')[1]
        districtName = domain.split('.')[0]

        district = Districts(district = districtName, emailDomain = domain, isIndependent = True)

        district.save()

        return district

    def addSignupUserToMailChimp(self,user):
        mailchimp = Client()
        mailchimp.set_config({
            "api_key": api_key,
            "server": server,
        })
        member_info = {
            "email_address": user.email,
            "status": "unsubscribed",
            "merge_fields": {
                "FNAME": user.first_name,
                "LNAME": user.last_name,
                "MMERGE8":user.teacher.district.district,
                "SCHOOL":user.teacherschool,
                "STATE":user.state,
                "MMERGE11":"Yes"
                }
        }
        try:
            response = mailchimp.lists.add_list_member(list_id, member_info)
            print("response: {}".format(response))
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))

    def clean(self):
        
        if User.objects.filter(username__exact=self.cleaned_data['username']).exists():
            raise forms.ValidationError(
                "Username already exists"
            )
        
        

        if User.objects.filter(email__exact=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                "Email address already exists"
            )

        
        return self.cleaned_data
                
# Form to select a school

class SelectSchoolForm(forms.Form):

    school = forms.CharField(max_length=100)

# Form to select a team for user

class FinishSignUpForm(forms.Form):

    team = forms.CharField(max_length=50)

class SubscribeForm(forms.Form):

    order = forms.ModelChoiceField(queryset=Subscriptions.objects)

class HealthDataForm(forms.Form):

    GENDER = [('Male', 'Male'), ('Female', 'Female')]
    CLOSED = [('No', 'No'), ('Yes', 'Yes')]

    GENDER_R = ['Male', 'Female']
    CLOSED_R = ['No', 'Yes']
    
    gender = forms.ChoiceField(choices=GENDER)
    birthday = forms.DateField()
    weight = forms.FloatField()
    height = forms.FloatField()
    sysBloodPressure = forms.FloatField(required=False)
    diasBloodPressure = forms.FloatField(required=False)
    cholesterol = forms.FloatField(required=False)
    waistsize = forms.FloatField()
    isPrediabetic = forms.ChoiceField(choices=CLOSED)
    isDiabetic = forms.ChoiceField(choices=CLOSED)
    isKeto = forms.BooleanField(required=False)
    lastDiet = forms.CharField(max_length=30, required=False)
    nutritionDetails = forms.CharField(max_length=1000, required=False)
    beforePicture = forms.ImageField(required=False)
    currentPicture = forms.ImageField(required=False)
    

class MacronutrientsForm(forms.Form):

    activityLevel = forms.ChoiceField(choices=Teacher.ACTIVITY_LEVEL)
    goal = forms.ChoiceField(choices=Teacher.GOAL_OPTIONS)


class EditMyProfileForm(forms.Form):
    
    profilePicture = forms.ImageField(required=False)
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=80)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

