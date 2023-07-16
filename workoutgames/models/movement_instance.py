from django.db import models
from .movement import Movement
from .pathInstance import PathInstance

class MovementInstance(models.Model):

    """
    Model that connect Movements with Gamers. When a Gamer accesses a Movement
    a MovementInstance instance is created

    Attributes:
        movement(ManyToOne): Many to one relationship to Movement
        recommended_reps(Integer): Number of reps calculated based on trainer input 
        recommended_sets(Integer): Number of sets calculated based on trainer input 
        recommended_weight(Float): Weight calculated based on trainer input 
        completed_sets(Integer): Number of sets actually completed by gamer
        date_completed(DateTime): Date when movement was completed
        path_instance(ManyToOne): Many to one relationship to PathInstance
        complete(Boolean): True if movement has been completed by user

    """

    recommended_reps = models.IntegerField(default=0)
    recommended_sets = models.IntegerField(default=0)
    recommended_weight = models.FloatField(default=0)
    completed_sets = models.IntegerField(default=0)
    date_completed = models.DateTimeField()
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE)
    path_instance = models.ForeignKey(PathInstance, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def calculate_numbers(self, gamer):

        """
        Adjust initial number of reps, sets, and weight to gamers record of
        completion

        Parameters:
            gamer(Gamer): Gamer accessing movement

        Returns:
            Void
        """

        self.recommended_reps = self.movement.base_reps
        self.recommended_sets = self.movement.base_sets
        self.recommended_weight = self.movement.base_weight

        self.save()

    def complete_movement(self):

        """
        Completes the movement
        """

        self.complete = True
        self.save()

    # def __str__(self):

    #     """
    #     Returns name of movement type as string
    #     """

    #     return self.name