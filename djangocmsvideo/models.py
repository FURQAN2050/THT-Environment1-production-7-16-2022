from django.db import models
from django import forms
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

# Create your models here.
from cms.models.pluginmodel import CMSPlugin

class Data(CMSPlugin):

    def copy_relations(self, oldinstance):
        # Before copying related objects from the old instance, the ones
        # on the current one need to be deleted. Otherwise, duplicates may
        # appear on the public version of the page
        self.associated_item.all().delete()

        for associated_item in oldinstance.associated_item.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            associated_item.pk = None
            associated_item.data = self
            associated_item.save()

class Video(models.Model):
    video = models.CharField(max_length=500)
    caption = HTMLField(default="", null=True, blank=True, max_length=1000)
    data = models.ForeignKey(Data, related_name="associated_item", on_delete=models.CASCADE ,null=True)