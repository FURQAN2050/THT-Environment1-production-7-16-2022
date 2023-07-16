from django.db import models
from .movement_instance import MovementInstance
from .pathInstance import PathInstance

class Set(models.Model):

    """
    Model that represents finished sets

    Attributes:
        completed_reps(Integer): Number of reps actually completed by gamer
        set_num(Integer): Order in which such set was completed
        used_weight(Float): Weight actually completed by gamer
        date_completed(DateTime): Date when movement was completed
        movement_instance(MovementInstance): Movement Instance associated with the set

    """
    
    completed_reps = models.IntegerField(default=0)
    set_num = models.IntegerField(default=0)
    used_weight = models.FloatField(default=0)
    date_completed = models.DateTimeField()
    movement_instance = models.ForeignKey(MovementInstance, on_delete=models.CASCADE)