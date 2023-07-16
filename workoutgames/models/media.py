from django.db import models
from django.utils import timezone
from django.conf import settings
from django.forms import ValidationError
from PIL import Image
from io import BytesIO
import pytz

from tools.mediaAbs import MediaAbs

def user_directory_path(instance, filename):

    """
    Returns path to save file model for image and video files
    file will be uploaded to 
    <media_folder>/content/<model>/user_<id>/<year>/<month>/<day>/
    """

    return 'workoutgames/{0}/user_{1}/{2}/{3}/{4}/{5}'.format(
        type(instance).__name__,
        instance.added_by.id,
        timezone.localtime(timezone.now(), pytz.timezone('US/Eastern')).year,
        timezone.localtime(timezone.now(), pytz.timezone('US/Eastern')).month,
        timezone.localtime(timezone.now(), pytz.timezone('US/Eastern')).day,
        str(instance.id) + "_"  + filename
        )

class MediaWorkout(MediaAbs):

    """
    Model that holds multimedia infomration

    Attributes:
        date(Datetime): Date when the value was created
        name(String): Name of the media
        thumbnail(ImageField): Thumbnail from media uploaded
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

        super(MediaWorkout, self).save(*args, **kwargs)

        


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


class ImageWorkout(MediaWorkout):

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

        super(ImageWorkout, self).save(*args, **kwargs)

        

class VideoWorkout(MediaWorkout):

    """
    Model that holds a video

    Attributes:
        video(File): Video file
    """

    video_field = models.FileField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):

        """
        Validates that a current file does not exist with the same file name
        and creates thumbnail
        """

        # Confirm that no more videos with the same name exist

        super(VideoWorkout, self).save(*args, **kwargs)

        # Create thumbnail

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
            
def extraSaveForImages(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:

        instance.convertImageFieldToJPEG()
        instance.saveThumbnailForImage(instance.image_field.url, instance.name, (512,512))

def extraSaveForVideos(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:

        instance.saveFrameForVideo(instance.video_field.url, instance.name, (512,512))


def videoPreSave(**kwargs):

    instance = kwargs.get('instance')

    if instance.checkVideoType() != True:

        raise ValidationError("Incorrect format")
    

models.signals.pre_delete.connect(video_delete_files, VideoWorkout)
models.signals.pre_delete.connect(image_delete_files, ImageWorkout)
models.signals.pre_save.connect(videoPreSave, VideoWorkout)
models.signals.post_save.connect(extraSaveForImages, ImageWorkout)
models.signals.post_save.connect(extraSaveForVideos, VideoWorkout)