from django.db import models

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as img
import requests
from io import StringIO, BytesIO
import cv2
import os
import magic as mg

class MediaAbs(models.Model):

    """
    Abstract model that includes common tools for media related models

    Defines:
        date(Datetime): Date when the value was created
        name(String): Name of the media
        thumbnail(ImageField): Thumbnail from media uploaded
        addedBy(ForeignKey): User that uploaded file
    """

    class Meta:

        abstract = True

    def getThumbnailFromImage(self, imageName, newName, size):

        """
        Provides a resized image of specified size from an image in a directory

        Parameters: 
            imageName(String) : Address to image to resize
            size(Integer[2]) : Size for image
          
        Returns: 
            Image: New image of size
        """

        response = requests.get(imageName)

        img_data = response.content

        image = img.open(BytesIO(img_data))

        # Convert to size

        image.thumbnail(size)

        b = BytesIO()

        image.save(b, 'JPEG')

        thumb_file = InMemoryUploadedFile(b, None, newName, 'image/jpeg', b.getbuffer().nbytes, None)

        return thumb_file

    def getFrameFromVideo(self, video, newName, size):

        """
        Extrats a frame from the middle of the video and saves it in jpg format

        Parameters: 
            video(String) : Address to video
          
        Returns: 
            String: Address to extracted image
        """

        print("1")

        # Open video
        cv2_video = cv2.VideoCapture(video)

        print("2")

        # Grab number of frames
        cv2_video.set(cv2.CAP_PROP_POS_AVI_RATIO,1)

        frames = cv2_video.get(cv2.CAP_PROP_POS_FRAMES)

        print("3")

        # Identify middle frame
        half_frames = frames / 2

        print("4")

        cv2_video.set(1,half_frames)

        print("5")

        # Record middle frame
        ret, frame = cv2_video.read()

        print("6")

        b = BytesIO()

        # Save frame

        is_success, buffer = cv2.imencode(".jpg", frame)
        b = BytesIO(buffer)

        print("7")

        image = img.open(b)

        print("8")

        # Convert to size

        image.thumbnail(size)

        print("9")

        b = BytesIO()

        image.save(b, 'JPEG')

        print("10")

        thumb_file = InMemoryUploadedFile(b, None, newName, 'image/jpeg', b.getbuffer().nbytes, None)

        print("11")

        return thumb_file


    def isImageJPG(self, image):

        whatType =  mg.from_buffer(image)

        print(whatType)

        if whatType[:3] == 'PNG':

            return False

        elif whatType[:4] == 'JPEG':

            return True

        else:
            raise Exception("Image is not JPEG or PNG")

        
    def isVideoMP4(self, video):

        whatType =  mg.from_buffer(video)

        print("Type: ", whatType)

        if whatType[11:14] == 'MP4':

            return True

        else:
            return False

    
    def isDocPDF(self, document):

        whatType = mg.from_buffer(document)

        print("Type: ", whatType[:3])

        if whatType[:3] == 'PDF':

            return True

        else:

            return False

