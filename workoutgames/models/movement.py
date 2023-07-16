from django.db import models
from .movement_type import MovementType
from django.utils import timezone


class Movement(models.Model):

    """
    Model to represent a type of movement

    Attributes:
        movement_type(ManyToOne): Many to One relationship with Movement Type
        base_reps(Integer): Base number of reps to be adjusted based on algorithm
        base_sets(Integer): Base number of sets to be adjusted based on algorithm
        base_weight(Float): Base weight to be later adjusted based on algorithm
        use_autocalculation_algorithm(Boolean): Whether to use the autocalculation algorithm
            to adjust initial number of reps, sets, and weight to gamers record of
            completion
        order(Integer): Order in which movement is to be presented
    """

    movement_type = models.ForeignKey(MovementType, on_delete=models.CASCADE)
    base_reps = models.IntegerField(default=1)
    base_sets = models.IntegerField(default=1)
    base_weight = models.FloatField(default=1)
    circuit = models.IntegerField(default=1)
    use_autocalculation_algorithm = models.BooleanField(default=True)
    datePosted = models.DateTimeField(default=timezone.datetime(2020, 1, 1))
    order = models.IntegerField(default=1)
    #workout = models.ForeignKey(WorkoutPlace, on_delete=models.CASCADE, default=None)

    def __str__(self):

        """
        Returns name of movement type as string
        """

        return self.movement_type.name + str(self.base_reps) + str(self.base_sets) + str(self.base_weight)

    def save(self, *args, **kwargs):

        """
        Sets posted date for object
        """

        if not self.id:
            self.datePosted = timezone.now()

        super(Movement, self).save(*args, **kwargs)