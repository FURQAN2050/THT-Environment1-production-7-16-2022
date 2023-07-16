from django.test import TestCase
from django.test.client import Client
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import datetime

from .models import Question, QuestionInstance
from accounts.models import User, Teacher, Teams, Districts

# Create your tests here.

USERNAME = 'lsavast'
PASSWORD = 'Leon1111'

class HabitsAPITraditionalTestCase(TestCase):

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
            question = Question()
            question.id = i
            question.question="Test question " + str(i)
            question.order = i
            question.save()

    def test_question_of_day_user_first_time(self):

        question = Question.objects.filter(id=1)[0]
        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['questions'][0] == "Test question 1")

    def test_question_of_day_after_answering_question_second_day(self):

        question = Question.objects.filter(id=1)[0]
        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})
        question.answerQuestion(True, user.trainee)
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]
        questionInstance.dateCreated = questionInstance.dateCreated - datetime.timedelta(2)
        questionInstance.save()
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['questions'][0] == "Test question 2")

    def test_question_of_day_two_question_same_order(self):

        question = Question.objects.filter(id=1)[0]
        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})
        question.answerQuestion(True, user.trainee)
        question = Question.objects.filter(id=2)[0]
        question.order = 1
        question.save()
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['questions'][0] == "Test question 2" or response.data['questions'][1] == "Test question 2")

    def test_question_of_day_no_questions_left_last_answer_today(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        for question in Question.objects.all():
            question.answerQuestion(True, user.trainee)
        
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['questions'][0] == "Test question 10")

    def test_question_of_day_no_questions_left_last_answer_yesterday(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        for question in Question.objects.all():
            question.answerQuestion(True, user.trainee)
            questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]
            questionInstance.dateCreated = questionInstance.dateCreated - datetime.timedelta(1)
            questionInstance.save()
        
        response = self.client.post('/habits/api/data/', {'action':'requestQuestionOfDay', 'userId' : user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['questions']) == 0)


    def test_request_question_routine(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestion', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['question'] == "Test question 1")


    def test_request_question_routine_repeat(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestion', 'id' : 4})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['question'] == "Test question 4")


    def test_request_question_not_in_database(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'requestQuestion', 'id' : 11})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_answer_question_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, True)
        self.assertEqual(user.trainee.points, question.points)


    def test_answer_question_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, False)
        self.assertEqual(user.trainee.points, 0)

    def test_answer_question_change_false_to_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, True)
        self.assertEqual(user.trainee.points, question.points)


    def test_answer_question_change_true_to_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, False)
        self.assertEqual(user.trainee.points, 0)

    def test_answer_question_change_true_to_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, True)
        self.assertEqual(user.trainee.points, question.points)


    def test_answer_question_change_false_to_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        question = Question.objects.filter(id=1)[0]
        questionInstance = QuestionInstance.objects.filter(question = question, trainee = user.trainee)[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(questionInstance.answer, False)
        self.assertEqual(user.trainee.points, 0)


    def test_is_question_answered_true_answer_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'isQuestionAnswered', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isAnswered'], True)


    def test_is_question_answered_true_answer_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        response = self.client.post('/habits/api/data/', {'action':'isQuestionAnswered', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isAnswered'], True)


    def test_is_question_answered_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'isQuestionAnswered', 'id' : 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['isAnswered'], False)


    def test_is_question_answered_question_does_not_exist(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 2, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 3, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'isQuestionAnswered', 'id' : 11})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_can_answer_question_answered(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'canAnswerQuestion', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['canAnswer'], True)


    def test_can_answer_question_unanswered_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'canAnswerQuestion', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['canAnswer'], True)

    
    def test_can_answer_question_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'canAnswerQuestion', 'id' : 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['canAnswer'], False)


    def test_can_answer_question_not_in_db(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'canAnswerQuestion', 'id' : 11})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_question_answer_true(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 1})
        response = self.client.post('/habits/api/data/', {'action':'getQuestionAnswer', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], True)


    def test_get_question_answer_false(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'answerQuestion', 'id' : 1, 'answer' : 0})
        response = self.client.post('/habits/api/data/', {'action':'getQuestionAnswer', 'id' : 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], False)

        
    def test_get_question_answer_none(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'getQuestionAnswer', 'id' : 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], None)


    def test_get_question_answer_question_not_in_db(self):

        user = User.objects.get(username='lsavast')
        response = self.client.post('/habits/api/data/', {'action':'getQuestionAnswer', 'id' : 11})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
