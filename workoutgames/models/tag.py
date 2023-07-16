from django.db import models

class Tag(models.Model):

    """
    Model that specifies descriptors

    Attributes:
        element(CharField): One word describing content
    """

    element = models.CharField(max_length=50)

    def __str__(self):

        return self.element

    class Meta:
        ordering = ('element',)