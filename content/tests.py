from django.test import TestCase
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from .models import Media, Image, Video, Content, Tag

from accounts.models import User

DATE = '2019/12/10'

MEDIA_SERVER = 'https://media-tht-test.s3.amazonaws.com/'

VIDEO_FILES = ["C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4",
            "C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4",
            "C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4"]

IMAGE_FILES = ["C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg",
            "C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg",
            "C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg"]

# Create your tests here.

class ImageUploadAndDeleteRoutineTestCase(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=my_admin.username, password=password)

        for index, image_file in enumerate(IMAGE_FILES):

            image = Image()

            image.name = "Image_" + str(index)
            image.added_by = my_admin
            image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
            image.save()

    def test_image_thumbnail(self):

        """Image uploads thumbnail to server correctly"""

        for index, image_file in enumerate(IMAGE_FILES):
        
            image = Image.objects.get(name="Image_" + str(index))
            self.assertEqual(image.thumbnail.url, MEDIA_SERVER + 'media/content/Image/user_1/' + DATE + '/' + str(image.id) + '_' + str(image.name) + '.thumbnail.jpg')
            self.assertEqual(image.image_field.url, MEDIA_SERVER + 'media/content/Image/user_1/' + DATE + '/' + str(image.id) + '_test_image.jpg')

    def tearDown(self):

        for index, image_file in enumerate(IMAGE_FILES):
        
            image = Image.objects.get(name="Image_" + str(index))
            image.delete()


class VideoUploadAndDeleteRoutineTestCase(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=my_admin.username, password=password)


        for index, video_file in enumerate(VIDEO_FILES):

            video = Video()

            video.name = "Video_" + str(index)
            video.added_by = my_admin
            video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video\mp4')
            video.save()

    def test_video_thumbnail(self):

        """Image uploads thumbnail to server correctly"""

        
        for index, video_file in enumerate(VIDEO_FILES):

            video = Video.objects.get(name="Video_" + str(index))
            self.assertEqual(video.thumbnail.url, MEDIA_SERVER + 'media/content/Video/user_1/' + DATE + '/' + str(video.id) + '_' + str(video.name) + '.thumbnail.jpg')
            self.assertEqual(video.video_field.url, MEDIA_SERVER + 'media/content/Video/user_1/' + DATE + '/' + str(video.id) + '_test_video.mp4')

    def tearDown(self):

        
        for index, video_file in enumerate(VIDEO_FILES):

            video = Video.objects.get(name="Video_" + str(index))
            video.delete()



class ContentUploadAndDeleteRoutineTestCase(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=my_admin.username, password=password)

        images = []
        videos = []

        for index, video_file in enumerate(VIDEO_FILES):

            video = Video()

            video.name = "Video_" + str(index)
            video.added_by = my_admin
            video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video\mp4')
            video.save()

            videos.append(video)

        for index, image_file in enumerate(IMAGE_FILES):

            image = Image()

            image.name = "Image_" + str(index)
            image.added_by = my_admin
            image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
            image.save()

            images.append(image)

        tag = Tag()

        tag.id = 1
        tag.element = "TestTag"

        tag.save()

        content = Content()

        content.id = 1
        content.name = "Content Test"
        content.description = "This is a test description"
        content.datePosted = timezone.now()

        content.save()

        content.tags.add(tag)

        
        for img in images:
            content.image_content.add(img)

        for vid in videos:
            content.video_content.add(vid)

        content.save()

    def test_content(self):

        """Image uploads thumbnail to server correctly"""

        content = Content.objects.get(name="Content Test")
        
        for index, video_file in enumerate(VIDEO_FILES):

            video = Video.objects.get(name="Video_" + str(index))
            
            self.assertEqual(content.video_content.get(name=video.name).thumbnail.url, MEDIA_SERVER + 'media/content/Video/user_1/' + DATE + '/' + str(video.id) + '_' + str(video.name) + '.thumbnail.jpg')
            self.assertEqual(content.video_content.get(name=video.name).video_field.url, MEDIA_SERVER + 'media/content/Video/user_1/' + DATE + '/' + str(video.id) + '_test_video.mp4')
        
        
        for index, image_file in enumerate(IMAGE_FILES):
        
            image = Image.objects.get(name="Image_" + str(index))

            self.assertEqual(content.image_content.get(name=image.name).thumbnail.url, MEDIA_SERVER + 'media/content/Image/user_1/' + DATE + '/' + str(image.id) + '_' + str(image.name) + '.thumbnail.jpg')
            self.assertEqual(content.image_content.get(name=image.name).image_field.url, MEDIA_SERVER + 'media/content/Image/user_1/' + DATE + '/' + str(image.id) + '_test_image.jpg')

        
        

    def tearDown(self):

        
        for index, video_file in enumerate(VIDEO_FILES):

            video = Video.objects.get(name="Video_" + str(index))
            video.delete()
        
        for index, image_file in enumerate(IMAGE_FILES):
        
            image = Image.objects.get(name="Image_" + str(index))
            image.delete()
        
        content = Content.objects.get(name="Content Test")
        content.delete()