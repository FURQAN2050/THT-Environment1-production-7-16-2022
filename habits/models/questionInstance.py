from django.db import models


class QuestionInstance(models.Model):

    """
    Model to represent the questions answered by each individual Teacher

    Attributes:

        answer(bool)
        dateAnswered(DateTimeField)
        question(foreignKey): Field with Question
        trainee(foreignKey): Field with Trainee

    """

    answer = models.BooleanField(null=True)
    dateCreated = models.DateTimeField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    trainee = models.ForeignKey('Trainee', on_delete=models.CASCADE)

    def setAnswer(self, answer):

        """
        Answers question

        Parameters:
            answer(boolean)

        """

        self.answer = answer