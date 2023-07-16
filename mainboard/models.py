from django.db import models

# Create your models here.

# Questions models for admins to add questions for teachers

# WORKON: Each question has different points

class Questions(models.Model):

    question = models.TextField()
    date = models.DateField()
    responses = models.PositiveIntegerField(default=0)
    yes = models.PositiveIntegerField(default=0)
    no = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Questions"

