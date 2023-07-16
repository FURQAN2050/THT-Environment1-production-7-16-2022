from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.exceptions import ValidationError
from django import forms
from django.template.defaultfilters import slugify

from django.core.files.uploadedfile import InMemoryUploadedFile

from tools.mediaAbs import MediaAbs

from PIL import Image as img
import requests
from io import StringIO, BytesIO
import cv2
import os
import re

# Create your models here.

def user_directory_path(instance, filename):

    """
    Returns path to save file model for image and video files
    file will be uploaded to 
    <media_folder>/content/<model>/user_<id>/<year>/<month>/<day>/
    """

    return 'content/{0}/user_{1}/{2}/{3}/{4}/{5}'.format(
        type(instance).__name__,
        instance.added_by.id,
        timezone.now().year,
        timezone.now().month,
        timezone.now().day,
        str(instance.id) + "_"  + filename
        )

def video_delete_files(**kwargs):

    """
    Remove files from a Video model
    """

    video = kwargs.get('instance')

    if video.video_field:

        # Remove video
        video.video_field.delete(False)

        if video.thumbnail:

            # Remove thumbnail
            video.thumbnail.delete(False)

        

def image_delete_files(**kwargs):

    """
    Remove files from a Image model
    """

    image = kwargs.get('instance')

    if image.image_field:

        # Remove image

        image.image_field.delete(False)

        if image.thumbnail:

            # Remove thumbnail
            image.thumbnail.delete(False)
    


class Media(MediaAbs):

    """
    Model that holds multimedia infomration

    Attributes:
        date(Datetime): Date when the value was created
        name(String): Name of the media
        thumbnai(ImageField): Thumbnail from media uploaded
        addedBy(ForeignKey): User that uploaded file
    """

    date = models.DateTimeField()
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to=user_directory_path, default=None)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):

        """
        Returns name of media as string
        """

        return self.name

    def save(self, *args, **kwargs):

        """
        Sets posted date for object
        """

        if not self.id:
            self.date = timezone.now()

        super(Media, self).save(*args, **kwargs)

        


    def saveThumbnailForImage(self, imageName, newName, size):

        """
        Provides a resized image of specified size from an image in a directory

        Parameters: 
            imageName(String) : Address to image to resize
            size(Integer[2]) : Size for image
          
        Returns: 
            Image: New image of size
        """

        name = newName + '.thumbnail.jpg'

        thumb_file = self.getThumbnailFromImage(imageName, name, size)

        self.thumbnail.save(name, thumb_file)

        return name

    def saveFrameForVideo(self, video, newName, size):

        """
        Extrats a frame from the middle of the video and saves it in jpg format

        Parameters: 
            video(String) : Address to video
          
        Returns: 
            String: Address to extracted image
        """

        name = newName + ".thumbnail.jpg"

        thumb_file = self.getFrameFromVideo(video, name, size)

        self.thumbnail.save(name, thumb_file)

        self.save()

        return name


    def convertImageFieldToJPEG(self):

        if self.image_field:

            if not self.isImageJPG(self.image_field.read()):

                name = self.name

                im = Image.open(self.image_field)
                rgb_im = im.convert('RGB')
                output = BytesIO()
                rgb_im.save(output, format='JPEG')
                self.image_field.delete()
                self.image_field.save(name + ".jpg", output, save=False)

    def checkVideoType(self):

        result = self.isVideoMP4(self.video_field.read())

        self.video_field.seek(0)

        return result


    def checkDocType(self):

        return self.isDocPDF(self.doc_field.read())


class Image(Media):

    """
    Model that holds an image

    Attributes:
        image(File): Image file
    """

    image_field = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """

        super(Image, self).save(*args, **kwargs)



class Video(Media):

    """
    Model that holds a video

    Attributes:
        video(File): Video file
    """

    # video_field_old = models.FileField(upload_to=user_directory_path, default=None, null=True, blank=True) # Kept for compatibility
    video_field = models.CharField(max_length=1000, default=None, null=True)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """
        
        super(Video, self).save(*args, **kwargs)

        # Create thumbnail

    def get_thumbnail(self):

        youtube_video_id = re.search("youtube\.com.*(/embed\/)(.{11})/?", self.video_field)
        return "http://img.youtube.com/vi/" + youtube_video_id.group(2) + "/0.jpg" if youtube_video_id != None else None


class Document(Media):

    """
    Model that holds a document

    Attributes:
        document(File): Document file pdf
    """

    doc_field = models.FileField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):
        
        super(Document, self).save(*args, **kwargs)

            


class Tag(models.Model):

    """
    Model that specifies descriptors

    Attributes:
        element(CharField): One word describing content
    """

    element = models.CharField(max_length=50)

    def __str__(self):

        return self.element


def validate_datetime(datetime):

    """
    Check if date is present or future

    Parameters:
        datetime(Datetime): Date to check
    """

    if datetime < timezone.now():
        raise ValidationError("Date cannot be in the past")
    

class Content(models.Model):

    """
    Model for multimedia content

    Attributes:
        name(String): Name for the content
        description(String): Text explaining content
        date(DateField): Date posted
        tags(Tag): Descriptors for the content
        image(Image): Images in content
        video(Video): Videos in content
        slug(SlugField): Unique link identifier
    """

    name = models.CharField(max_length=150)
    description = models.TextField()
    datePosted = models.DateTimeField(validators=[validate_datetime])
    sortOrder = models.IntegerField(default=100)
    tags = models.ManyToManyField(Tag, blank=True)
    image_content = models.ManyToManyField(Image, blank=True)
    video_content = models.ManyToManyField(Video, blank=True)
    doc_content = models.ManyToManyField(Document, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):

        """
        Creates unique link and date for content model
        """

        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
            self.datePosted = timezone.now()

        super(Content, self).save(*args, **kwargs)

    def getThumbnail(self):

        """
            Gets thumbnail from media
        """

        if len(self.image_content.all()) > 0:
            return self.image_content.all()[0].thumbnail.url

        elif len(self.video_content.all()) > 0:
            return self.video_content.all()[0].get_thumbnail()
        
        else:
            return None

    def search(self, searchtext):

        """
        Finds content objects based on text

        Parameters:
            searchtext(String): Text to search in content objexts

        Returns:
            List: Content objects
        """

        return self.objects.filter(name_icontains=searchtext)


    def __str__(self):

        """
        Name of the model
        
        Returns:
            String: Containing name
        """

        return self.name

        
def extraSaveForImages(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        
        instance.convertImageFieldToJPEG()
        instance.saveThumbnailForImage(instance.image_field.url, instance.name, (512,512))

def extraSaveForVideos(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    # if created:
        
    #     instance.saveFrameForVideo(instance.video_field.url, instance.name, (512,512))


def videoPreSave(**kwargs):

    instance = kwargs.get('instance')

    # if instance.checkVideoType() != True:

    #     raise forms.ValidationError("Incorrect format", code='invalid')


def documentPreSave(**kwargs):

    instance = kwargs.get('instance')

    if instance.checkDocType() == False:

        print(instance.checkDocType())

        raise ValidationError("Incorrect document format", code='invalid')



models.signals.pre_delete.connect(video_delete_files, Video)
models.signals.pre_delete.connect(image_delete_files, Image)
models.signals.pre_save.connect(documentPreSave, Document)
models.signals.pre_save.connect(videoPreSave, Video)
models.signals.post_save.connect(extraSaveForImages, Image)
models.signals.post_save.connect(extraSaveForVideos, Video)
