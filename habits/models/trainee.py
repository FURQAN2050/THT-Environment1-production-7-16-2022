from django.db import models

from .question import Question
from .questionInstance import QuestionInstance
from accounts.models import User


class Trainee(models.Model):

    """
    Model that represents a Trainee

    Attributes:
        User(OneToOne): One to one field to User
        points(Integer): Amount of points accumulated by trainee
        questionInstance(MainyToMany): Questions answered

    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

