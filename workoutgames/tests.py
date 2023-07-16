from django.test import TestCase
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.utils import timezone
from django.db.models import signals
from rest_framework.test import APIClient
from rest_framework import status

import datetime
import pytz

from accounts.models import User
from accounts.models import Teacher, Districts, Teams

from .models import ImageWorkout, VideoWorkout, Tag, Workout, Path, PathInstance, Gamer

from .models.media import extraSaveForImages, extraSaveForVideos, image_delete_files, video_delete_files

DATE = '2019/12/23'

MEDIA_SERVER = 'https://media-tht-test.s3.amazonaws.com/'

VIDEO_FILES = ["C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4",
            "C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4",
            "C:/Users/ellesse3.us/Documents/WebProjects/Freedom Fitness/web/media/Adobe XD 2019-08-19 16-16-28_2.mp4"]

IMAGE_FILES = ["C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg",
            "C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg",
            "C:/Users/ellesse3.us/Pictures/5-29-18/IMG_1126.jpg",
            "C:/Users/ellesse3.us/Pictures/Capture.png"]

# Create your tests here.



class ImageWorkoutTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

    def test_init_name_dot(self):

        image_file = IMAGE_FILES[0]

        image = ImageWorkout()

        image.name = "."
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
        image.save()

        imageSearch = ImageWorkout.objects.get(name=".")
        
        self.assertEqual(imageSearch.name, ".")
        self.assertEqual(imageSearch.added_by, self.my_admin)
        self.assertEqual(imageSearch.thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch.id) + '_' + str(imageSearch.name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch.image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch.id) + '_test_image.jpg')

        imageSearch.delete()

    def test_init_past_date(self):

        image_file = IMAGE_FILES[0]

        image = ImageWorkout()

        image.name = "test"
        image.date = datetime.date(2019,11,20)
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
        image.save()

        imageSearch = ImageWorkout.objects.get(name="test")
        
        self.assertEqual(imageSearch.name, "test")
        self.assertEqual(imageSearch.added_by, self.my_admin)
        self.assertEqual(imageSearch.thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch.id) + '_' + str(imageSearch.name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch.image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch.id) + '_test_image.jpg')

        imageSearch.delete()

    def test_init_existing_name(self):

        image_file = IMAGE_FILES[0]

        image = ImageWorkout()

        image.name = "test"
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
        image.save()

        image = ImageWorkout()

        image.name = "test"
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
        image.save()

        imageSearch = ImageWorkout.objects.filter(name="test")

        self.assertEqual(imageSearch[0].name, "test")
        self.assertEqual(imageSearch[0].added_by, self.my_admin)
        self.assertEqual(imageSearch[0].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_' + str(imageSearch[0].name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch[0].image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_test_image.jpg')


        self.assertEqual(imageSearch[1].name, "test")
        self.assertEqual(imageSearch[1].added_by, self.my_admin)
        self.assertEqual(imageSearch[1].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[1].id) + '_' + str(imageSearch[1].name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch[1].image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[1].id) + '_test_image.jpg')

        imageSearch[1].delete()
        imageSearch[0].delete()


    def test_init_png(self):

        image_file = IMAGE_FILES[3]

        image = ImageWorkout()

        image.name = "test1png"
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.png', content=open(image_file, 'rb').read(), content_type='image/png')
        image.save()

        imageSearch = ImageWorkout.objects.filter(name="test1png")

        self.assertEqual(imageSearch[0].name, "test1png")
        self.assertEqual(imageSearch[0].added_by, self.my_admin)
        self.assertEqual(imageSearch[0].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_' + str(imageSearch[0].name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch[0].image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_test1png.jpg')


        imageSearch[0].delete()

    def test_delete_routine(self):

        image_file = IMAGE_FILES[0]

        image = ImageWorkout()

        image.name = "."
        image.added_by = self.my_admin
        image.image_field = SimpleUploadedFile(name='test_image.jpg', content=open(image_file, 'rb').read(), content_type='image/jpeg')
        image.save()

        imageSearch = ImageWorkout.objects.filter(name=".")

        self.assertEqual(imageSearch[0].name, ".")
        self.assertEqual(imageSearch[0].added_by, self.my_admin)
        self.assertEqual(imageSearch[0].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_' + str(imageSearch[0].name) + '.thumbnail.jpg')
        self.assertEqual(imageSearch[0].image_field.url, MEDIA_SERVER + 'media/workoutgames/ImageWorkout/user_1/' + DATE + '/' + str(imageSearch[0].id) + '_test_image.jpg')


        imageSearch[0].delete()

        imageSearch = ImageWorkout.objects.filter(name=".")

        self.assertEqual(len(imageSearch), 0)

class VideoWorkoutTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

    def test_init_name_dot(self):

        video_file = VIDEO_FILES[0]

        video = VideoWorkout()

        video.name = "."
        video.added_by = self.my_admin
        video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video/mp4')
        video.save()

        videoSearch = VideoWorkout.objects.get(name=".")
        
        self.assertEqual(videoSearch.name, ".")
        self.assertEqual(videoSearch.added_by, self.my_admin)
        self.assertEqual(videoSearch.thumbnail.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch.id) + '_' + str(videoSearch.name) + '.thumbnail.jpg')
        self.assertEqual(videoSearch.video_field.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch.id) + '_test_video.mp4')

        videoSearch.delete()

    def test_init_past_date(self):

        video_file = VIDEO_FILES[0]

        video = VideoWorkout()

        video.name = "test"
        video.date = datetime.date(2019,11,20)
        video.added_by = self.my_admin
        video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video/mp4')
        video.save()

        videoSearch = VideoWorkout.objects.get(name="test")
        
        self.assertEqual(videoSearch.name, "test")
        self.assertEqual(videoSearch.added_by, self.my_admin)
        self.assertEqual(videoSearch.thumbnail.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch.id) + '_' + str(videoSearch.name) + '.thumbnail.jpg')
        self.assertEqual(videoSearch.video_field.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch.id) + '_test_video.mp4')

        videoSearch.delete()

    def test_init_existing_name(self):

        video_file = VIDEO_FILES[0]

        video = VideoWorkout()

        video.name = "test"
        video.added_by = self.my_admin
        video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video/mp4')
        video.save()

        video = VideoWorkout()

        video.name = "test"
        video.added_by = self.my_admin
        video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video/mp4')
        video.save()

        videoSearch = VideoWorkout.objects.filter(name="test")

        self.assertEqual(videoSearch[0].name, "test")
        self.assertEqual(videoSearch[0].added_by, self.my_admin)
        self.assertEqual(videoSearch[0].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[0].id) + '_' + str(videoSearch[0].name) + '.thumbnail.jpg')
        self.assertEqual(videoSearch[0].video_field.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[0].id) + '_test_video.mp4')


        self.assertEqual(videoSearch[1].name, "test")
        self.assertEqual(videoSearch[1].added_by, self.my_admin)
        self.assertEqual(videoSearch[1].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[1].id) + '_' + str(videoSearch[1].name) + '.thumbnail.jpg')
        self.assertEqual(videoSearch[1].video_field.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[1].id) + '_test_video.mp4')

        videoSearch[1].delete()
        videoSearch[0].delete()

    def test_delete_routine(self):

        video_file = VIDEO_FILES[0]

        video = VideoWorkout()

        video.name = "."
        video.added_by = self.my_admin
        video.video_field = SimpleUploadedFile(name='test_video.mp4', content=open(video_file, 'rb').read(), content_type='video/mp4')
        video.save()

        videoSearch = VideoWorkout.objects.filter(name=".")

        self.assertEqual(videoSearch[0].name, ".")
        self.assertEqual(videoSearch[0].added_by, self.my_admin)
        self.assertEqual(videoSearch[0].thumbnail.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[0].id) + '_' + str(videoSearch[0].name) + '.thumbnail.jpg')
        self.assertEqual(videoSearch[0].video_field.url, MEDIA_SERVER + 'media/workoutgames/VideoWorkout/user_1/' + DATE + '/' + str(videoSearch[0].id) + '_test_video.mp4')


        videoSearch[0].delete()

        videoSearch = VideoWorkout.objects.filter(name=".")

        self.assertEqual(len(videoSearch), 0)



class WorkoutTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

        videoWorkoutFactory(3, 'workoutgames/VideoWorkout/user_1/2019/12/12/3_test_video.mp4', self.my_admin, thumbnail='workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg')

        imageWorkoutFactory(3, 'workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg', self.my_admin)


        for i in range(5):
            tag = Tag()
            tag.element = "tag" + str(i)
            tag.save()

        
    def test_init_routine(self):

        workout = Workout()
        tag = Tag.objects.get(element="tag1")

        workout.name = "Test 1"
        workout.description = "This is a test"
        workout.level = 1
        workout.datePosted = timezone.now()

        workout.save()

        workout.tag.add(tag)

        images = ImageWorkout.objects.all()
        videos = VideoWorkout.objects.all()

        for image in images:

            workout.image_content.add(image)
            
            
        for video in videos:
            workout.video_content.add(video)

        
        workoutSearch = Workout.objects.filter(name="Test 1")

        self.assertEqual(len(workoutSearch), 1)
        self.assertEqual(workoutSearch[0].name, "Test 1")
        self.assertEqual(workoutSearch[0].description, "This is a test")
        self.assertEqual(workoutSearch[0].level, 1)
        self.assertEqual(workoutSearch[0].tag.all().count(), 1)
        self.assertEqual(workoutSearch[0].image_content.all().count(), len(images))
        self.assertEqual(workoutSearch[0].video_content.all().count(), len(videos))

        workoutSearch[0].delete()

    def test_init_no_tag(self):

        workout = Workout()
        tag = Tag.objects.get(element="tag1")

        workout.name = "Test 1"
        workout.description = "This is a test"
        workout.level = 1
        workout.datePosted = timezone.now()

        workout.save()

        images = ImageWorkout.objects.all()
        videos = VideoWorkout.objects.all()

        for image in images:

            workout.image_content.add(image)
            
            
        for video in videos:
            workout.video_content.add(video)

        
        workoutSearch = Workout.objects.filter(name="Test 1")

        self.assertEqual(len(workoutSearch), 1)
        self.assertEqual(workoutSearch[0].name, "Test 1")
        self.assertEqual(workoutSearch[0].description, "This is a test")
        self.assertEqual(workoutSearch[0].level, 1)
        self.assertEqual(workoutSearch[0].image_content.all().count(), len(images))
        self.assertEqual(workoutSearch[0].video_content.all().count(), len(videos))

        workoutSearch[0].delete()

    def test_init_routine(self):

        workout = Workout()
        tag = Tag.objects.get(element="tag1")

        workout.name = "Test 1"
        workout.description = "This is a test"
        workout.level = 1
        workout.datePosted = datetime.date(2019,11,20)

        workout.save()

        workout.tag.add(tag)

        images = ImageWorkout.objects.all()
        videos = VideoWorkout.objects.all()

        for image in images:

            workout.image_content.add(image)
            
            
        for video in videos:
            workout.video_content.add(video)

        
        workoutSearch = Workout.objects.filter(name="Test 1")

        self.assertEqual(len(workoutSearch), 1)
        self.assertEqual(workoutSearch[0].name, "Test 1")
        self.assertEqual(workoutSearch[0].description, "This is a test")
        self.assertEqual(workoutSearch[0].level, 1)
        self.assertEqual(workoutSearch[0].tag.all().count(), 1)
        self.assertEqual(workoutSearch[0].datePosted, datetime.datetime(2019,11,20,0,0, tzinfo=pytz.UTC))
        self.assertEqual(workoutSearch[0].image_content.all().count(), len(images))
        self.assertEqual(workoutSearch[0].video_content.all().count(), len(videos))

        workoutSearch[0].delete()


    def test_delete_routine(self):

        workout = Workout()
        tag = Tag.objects.get(element="tag1")

        workout.name = "Test 1"
        workout.description = "This is a test"
        workout.level = 1
        workout.datePosted = timezone.now()

        workout.save()

        workout.tag.add(tag)

        images = ImageWorkout.objects.all()
        videos = VideoWorkout.objects.all()

        for image in images:

            workout.image_content.add(image)
            
            
        for video in videos:
            workout.video_content.add(video)

        workout.save()

        workout.delete()
        
        workoutSearch = Workout.objects.filter(name="Test 1")

        self.assertEqual(len(workoutSearch), 0)


class PathTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

        videoWorkoutFactory(3, 'workoutgames/VideoWorkout/user_1/2019/12/12/3_test_video.mp4', self.my_admin, thumbnail='workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg')

        imageWorkoutFactory(3, 'workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg', self.my_admin)

        images = list(ImageWorkout.objects.all())
        videos = list(VideoWorkout.objects.all())


        for i in range(5):
            tag = Tag()
            tag.element = "tag" + str(i)
            tag.save()

        tags = list(Tag.objects.all())

        for i in range(5):

            workoutFactory("Test_" + str(i), images, videos, tags, level=i)


    def test_init_routine(self):

        path = Path()

        workouts = list(Workout.objects.all())

        path.name = "Test 1"
        path.description = "This is a test"

        path.save()

        path.workout.add(*workouts)

        path.save()

        pathSearch = Path.objects.filter(name="Test 1")

        self.assertEqual(pathSearch[0].name, "Test 1")
        self.assertEqual(pathSearch[0].description, "This is a test")
        self.assertEqual(pathSearch[0].workout.all().count(), 5)

        path.delete()

    def test_init_routine_no_workouts(self):

        path = Path()

        workouts = list(Workout.objects.all())

        path.name = "Test 1"
        path.description = "This is a test"

        path.save()

        pathSearch = Path.objects.filter(name="Test 1")

        self.assertEqual(pathSearch[0].name, "Test 1")
        self.assertEqual(pathSearch[0].description, "This is a test")
        self.assertEqual(pathSearch[0].workout.all().count(), 0)

        path.delete()


    def test_delete(self):

        path = Path()

        workouts = list(Workout.objects.all())

        path.name = "Test 1"
        path.description = "This is a test"

        path.save()

        path.workout.add(*workouts)

        path.save()

        path.delete()

        pathSearch = Path.objects.filter(name="Test 1")

        self.assertEqual(len(pathSearch), 0)


    def test_createPathInstance_routine_empty(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = path.createPathInstance()

        self.assertEqual(pathInstance.path, path)

    def test_createPathInstance_routine_2_instances(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = path.createPathInstance()

        pathInstance = path.createPathInstance()

        self.assertEqual(pathInstance.path, path)
        self.assertEqual(path.pathinstance_set.all().count(), 2)

    def test_createPathInstance_routine_3_instances(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = path.createPathInstance()
        pathInstance = path.createPathInstance()
        pathInstance = path.createPathInstance()

        self.assertEqual(pathInstance.path, path)
        self.assertEqual(path.pathinstance_set.all().count(), 3)


    def test_canUserAccessWorkout_no_path_instance(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        gamer = Gamer()
        gamer.user = self.my_admin
        
        gamer.save()

        workouts = list(Workout.objects.all())

        workout = workouts[0]
        path.workout.add(workout)

        canAccess = True
        canAccess = path.canUserAccessWorkout(gamer, workout)

        self.assertEqual(canAccess, False)

    def test_canUserAccessWorkout_gamer_workout_contains_workoutInstance(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = PathInstance()
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = path
        pathInstance.currentLevel = 4
        pathInstance.save()

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        gamer.path.add(pathInstance)
        gamer.save()

        workouts = list(Workout.objects.all())

        workout = workouts[0]
        
        path.workout.add(workout)
        path.save()

        pathInstance.workout.add(workout)
        pathInstance.save()

        canAccess = False
        canAccess = path.canUserAccessWorkout(gamer, workout)

        self.assertEqual(canAccess, True)

    def test_canUserAccessWorkout_gamer_not_requried_level(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = PathInstance()
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = path
        pathInstance.currentLevel = 1
        pathInstance.save()

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        gamer.path.add(pathInstance)
        gamer.save()

        workout = Workout.objects.get(level=3)
        
        path.workout.add(workout)
        path.save()

        canAccess = True
        canAccess = path.canUserAccessWorkout(gamer, workout)

        self.assertEqual(canAccess, False)

    
    def test_canUserAccessWorkout_gamer_not_requried_level(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = PathInstance()
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = path
        pathInstance.currentLevel = 3
        pathInstance.save()

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        gamer.path.add(pathInstance)
        gamer.save()

        workouts = []

        for i in range(4):

            workouts.append(Workout.objects.get(level=i))
        
        path.workout.add(workout[0], workout[1], workout[2], workout[3])
        path.save()

        pathInstance.workout.add(workout[0], workout[1])
        pathInstance.save()

        canAccess = False
        canAccess = path.canUserAccessWorkout(gamer, workout[3])

        self.assertEqual(canAccess, True)

    def test_canUserAccessWorkout_gamer_not_requried_level(self):

        path = Path()
        path.name = "Test 1"
        path.description = "This is a test"
        path.save()

        pathInstance = PathInstance()
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = path
        pathInstance.currentLevel = 3
        pathInstance.save()

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        gamer.path.add(pathInstance)
        gamer.save()

        workouts = []

        for i in range(4):

            workouts.append(Workout.objects.get(level=i))
        
        path.workout.add(workouts[0], workouts[1], workouts[2], workouts[3])
        path.save()

        pathInstance.workout.add(workouts[0], workouts[1], workouts[3])
        pathInstance.save()

        canAccess = False
        canAccess = path.canUserAccessWorkout(gamer, workouts[2])

        self.assertEqual(canAccess, True)


class PathInstanceTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

        videoWorkoutFactory(3, 'workoutgames/VideoWorkout/user_1/2019/12/12/3_test_video.mp4', self.my_admin, thumbnail='workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg')

        imageWorkoutFactory(3, 'workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg', self.my_admin)

        images = list(ImageWorkout.objects.all())
        videos = list(VideoWorkout.objects.all())


        for i in range(5):
            tag = Tag()
            tag.element = "tag" + str(i)
            tag.save()

        tags = list(Tag.objects.all())

        for i in range(5):

            workoutFactory("Test_" + str(i), images, videos, tags, level=i)

        workouts = Workout.objects.all()

        for i in range(3):

            path = Path()
            path.name = "Path " + str(i)
            path.description = "This is path " + str(i)

            path.save()

            path.workout.add(workouts[i], workouts[(i+1)%3])
        
            path.save()

    def test_init_routine_workouts_empty(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        pathInstanceSearch = PathInstance.objects.all()

        self.assertEqual(pathInstanceSearch[0].path.name, "Path 1")
        self.assertEqual(pathInstanceSearch[0].currentLevel, 0)

        pathInstanceSearch[0].delete()

    def test_init_routine_workouts(self):

        path = Path.objects.get(name="Path 2")
        workouts = Workout.objects.all()

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()

        pathInstance.path = path

        pathInstance.save()

        pathInstance.workout.add(workouts[0], workouts[1])

        pathInstance.save()

        pathInstanceSearch = PathInstance.objects.all()

        self.assertEqual(pathInstanceSearch[0].path.name, "Path 2")
        self.assertEqual(pathInstanceSearch[0].currentLevel, 0)
        self.assertEqual(pathInstanceSearch[0].workout.all().count(), 2)

        pathInstanceSearch[0].delete()

        

    def test_delete_routine_workouts(self):

        path = Path.objects.get(name="Path 2")
        workouts = Workout.objects.all()

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()

        pathInstance.path = path

        pathInstance.save()

        pathInstance.workout.add(workouts[0], workouts[1])

        pathInstance.save()

        pathInstance.delete()

        pathInstanceSearch = PathInstance.objects.all()

        self.assertEqual(len(pathInstanceSearch), 0)


    def test_delete_routine_no_workouts(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        pathInstance.delete()

        pathInstanceSearch = PathInstance.objects.all()

        self.assertEqual(len(pathInstanceSearch), 0)

    def test_addCompletedWorkout_routine(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        workout = Workout.objects.filter(path__id=path.id)

        pathInstance.addWorkout(workout[0])

        pathInstance.save()

        workoutSearch = Workout.objects.filter(pathinstance__id=pathInstance.id)

        self.assertEqual(workoutSearch[0].id, workout[0].id)
        self.assertEqual(len(workoutSearch), 1)

    def test_addCompletedWorkout_routine_2_workouts(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        workout = Workout.objects.filter(path__id=path.id)

        pathInstance.addWorkout(workout[0])
        pathInstance.addWorkout(workout[1])

        pathInstance.save()

        workoutSearch = Workout.objects.filter(pathinstance__id=pathInstance.id)

        self.assertEqual(len(workoutSearch), 2)

    def test_isPathComplete_empty(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        workout = Workout.objects.filter(path__id=path.id)

        pathInstance.addWorkout(workout[1])
        pathInstance.addWorkout(workout[2])

        pathInstance.save()

        pathCompleted = pathInstance.isPathComplete()

        self.assertEqual(pathCompleted, True)

    def test_isPathComplete_empty(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        workout = Workout.objects.filter(path__id=path.id)

        pathInstance.addWorkout(workout[1])

        pathInstance.save()

        pathCompleted = pathInstance.isPathComplete()

        self.assertEqual(pathCompleted, False)



    def test_isPathComplete_empty(self):

        path = Path.objects.get(name="Path 1")

        pathInstance = PathInstance()

        pathInstance.dateStarted = timezone.now()
        
        pathInstance.path = path

        pathInstance.save()

        workout = Workout.objects.filter(path__id=path.id)

        pathInstance.save()

        pathCompleted = pathInstance.isPathComplete()

        self.assertEqual(pathCompleted, False)


class GamerTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword'

        self.my_admin = userFactory(password, 'myuser2', 'myemail@test.com')

        c = Client()

        # You'll need to log him in before you can send requests through the client
        c.login(username=self.my_admin.username, password=password)

        videoWorkoutFactory(3, 'workoutgames/VideoWorkout/user_1/2019/12/12/3_test_video.mp4', self.my_admin, thumbnail='workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg')

        imageWorkoutFactory(3, 'workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg', self.my_admin)

        images = list(ImageWorkout.objects.all())
        videos = list(VideoWorkout.objects.all())


        for i in range(5):
            tag = Tag()
            tag.element = "tag" + str(i)
            tag.save()

        tags = list(Tag.objects.all())

        for i in range(1,6):

            workoutFactory("Test_" + str(i), images, videos, tags, level=i, myId=i)

        workoutFactory("Test_6", images, videos, tags, level=2, myId=6)

        for i in range(1,6,2):

            path = Path()
            path.name = "Path " + str(i)
            path.description = "This is path " + str(i)

            workout = Workout.objects.filter(id__lte=5)
            #workout2 = Workout.objects.get(id=(i+1))

            path.save()

            path.workout.add(*list(workout))
        
            path.save()

        Path.objects.get(name="Path 1").workout.add(Workout.objects.get(id=6))


    def test_accessPath_routine_user_has_paths(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        pathInstance = PathInstance()
        pathInstance.dateStarted = timezone.now()
        pathInstance.path = Path.objects.get(name="Path 1")
        pathInstance.save()

        gamer.path.add(pathInstance)

        gamer.save()

        path = Path.objects.get(name="Path 3")

        gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 2)
        
        raised = False
        
        try:
            PathInstance.objects.get(gamer=gamer, path=path)
        except:
            raised = True
        
        self.assertFalse(raised, 'Exception raised when attempting to find PathInstance in gamer')


    def test_accessPath_routine_user_paths_empty(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 1)
        
        raised = False
        
        try:
            PathInstance.objects.get(gamer=gamer, path=path)
        except:
            raised = True
        
        self.assertFalse(raised, 'Exception raised when attempting to find PathInstance in gamer')


    def test_accessPath_routine_user_in_path_already(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 1)

        path = Path.objects.get(name="Path 3")

        self.assertFalse(gamer.accessPath(path))

    def test_accessPath_routine_user_in_path_already_same_path(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 1)

        self.assertFalse(gamer.accessPath(path))



    def test_completeWorkout_routine_empty_workout_list(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        workout = Workout.objects.get(level=1, path__in=[path])

        gamer.accessPath(path)
        gamer.completeWorkout(path, workout)

        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)


        self.assertEqual(pathInstance.workout.all().count(), 1)
        self.assertEqual(pathInstance.currentLevel, 2)

        gamer = Gamer.objects.get(id=gamer.id)

        self.assertEqual(gamer.currLevelPath, 1)

    def test_completeWorkout_workout_higher_level(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        workout = Workout.objects.filter(level=2, path__in=[path])[0]

        gamer.accessPath(path)
        gamer.completeWorkout(path, workout)

        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        self.assertEqual(pathInstance.workout.all().count(), 0)
        self.assertEqual(pathInstance.currentLevel, 1)

        gamer = Gamer.objects.get(id=gamer.id)

        self.assertEqual(gamer.currLevelPath, 1)
    
    
    def test_completeWorkout_routine_more_than_workout_per_level(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        #import pdb; pdb.set_trace()

        path = Path.objects.get(name="Path 1")

        workout = Workout.objects.get(level=1)
        gamer.accessPath(path)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        self.assertEqual(pathInstance.currentLevel, 1)

        gamer.completeWorkout(path, workout, True)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        self.assertEqual(pathInstance.currentLevel, 2)

        workouts = Workout.objects.filter(level=2)
        gamer.completeWorkout(path, workouts[0], True)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        self.assertEqual(pathInstance.currentLevel, 2)

        gamer.completeWorkout(path, workouts[1], True)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        self.assertEqual(pathInstance.currentLevel, 3)

        gamer = Gamer.objects.get(id=gamer.id)

        self.assertEqual(gamer.currLevelPath, 1)


    def test_completeWorkout_increase_levelPath(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        workouts = path.workout.all()
        gamer.accessPath(path)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)
        pathInstance.currentLevel = 5
        pathInstance.save()

        for workout in workouts:
            gamer.completeWorkout(path, workout, True)

        path = Path.objects.get(name="Path 3")
        workouts = path.workout.all()
        gamer.accessPath(path)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)
        pathInstance.currentLevel = 5
        pathInstance.save()

        for workout in workouts:
            gamer.completeWorkout(path, workout, True)

        path = Path.objects.get(name="Path 5")
        workouts = path.workout.all()
        gamer.accessPath(path)
        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)
        pathInstance.currentLevel = 5
        pathInstance.save()

        for workout in workouts:
            gamer.completeWorkout(path, workout, True)


        gamer = Gamer.objects.get(id=gamer.id)

        self.assertEqual(gamer.currLevelPath, 2)

    def test_getPathInstance_one_path_instance(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")
        gamer.accessPath(path)

        path_instance = PathInstance.objects.get(path=path, gamer__in=[gamer])

        self.assertEqual(path_instance, gamer.getPathInstance(path))


    def test_getPathInstance_two_path_instances(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")
        gamer.accessPath(path)

        path = Path.objects.get(name="Path 3")

        self.assertEqual(None, gamer.getPathInstance(path))

    def test_getPathInstance_no_path_instances(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        self.assertEqual(None, gamer.getPathInstance(path))




class WorkoutControllerTest(TestCase):

    def setUp(self):

        # store the password to login later
        password = 'mypassword' 

        self.my_admin = User.objects.create_superuser('myuser2', 'myemail@test.com', password)

        teacher = Teacher()

        teacher.user = self.my_admin

        teacher.save()

        self.client = APIClient()

        # You'll need to log him in before you can send requests through the client
        self.client.login(username=self.my_admin.username, password=password)

        videoWorkoutFactory(3, 'workoutgames/VideoWorkout/user_1/2019/12/12/3_test_video.mp4', self.my_admin, thumbnail='workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg')

        imageWorkoutFactory(3, 'workoutgames/ImageWorkout/user_1/2019/12/12/4_test_image.jpg', self.my_admin)

        images = list(ImageWorkout.objects.all())
        videos = list(VideoWorkout.objects.all())


        for i in range(5):
            tag = Tag()
            tag.element = "tag" + str(i)
            tag.save()

        tags = list(Tag.objects.all())

        for i in range(1,7):

            workoutFactory("Test_" + str(i), images, videos, tags, level=i, myId=i)

        for i in range(1,6,2):

            path = Path()
            path.name = "Path " + str(i)
            path.description = "This is path " + str(i)

            path.save()

            workout1 = Workout.objects.get(level=i)
            workout2 = Workout.objects.get(level=i+1)

            path.workout.add(workout1, workout2)
        
            path.save()

    # WORKON: Expand test to review server responses

    def test_post_not_logged_in(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        client2 = APIClient()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.get(level=1)
        
        response = client2.post('/workoutgames/api/data/', {'action':'requestWorkoutOpen', 'workoutId': workout.id, 'userId': self.my_admin.id, 'pathId' : path.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        gamer.delete()

    def test_post_requestWorkoutOpen_accessible_by_gamer(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.get(level=1)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutOpen', 'workoutId': workout.id, 'userId': self.my_admin.id, 'pathId' : path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_requestWorkoutOpen_not_accessible_by_gamer(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.get(level=1)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutOpen', 'workoutId': workout.id, 'userId': self.my_admin.id, 'pathId' : path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_parameters_wrong(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.get(level=1)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'notAValidRequest', 'workoutId': workout.id, 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        gamer.delete()

    def test_post_requestWorkoutList_routine(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.get(level=1)

        gamer.completeWorkout(path, workout)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutList', 'pathId': path.id, 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_requestWorkoutList_all_available(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        
        for i in range(1,5):
            workout = Workout.objects.get(level=i)

            gamer.completeWorkout(path, workout)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutList', 'pathId': path.id, 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_requestWorkoutList_none_available(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutList', 'pathId': path.id, 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_requestWorkoutList_all_completed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        
        for i in range(1,6):
            workout = Workout.objects.get(level=i)

            gamer.completeWorkout(path, workout)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestWorkoutList', 'pathId': path.id, 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()


    def test_post_requestPaths_all_accessed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        paths = list(Path.objects.all())

        for path in paths:
            
            gamer.accessPath(path)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestPaths', 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()

    def test_post_requestPaths_some_accessed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")
            
        gamer.accessPath(path)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestPaths', 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()


    def test_post_requestPaths_none_accessed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()
        
        response = self.client.post('/workoutgames/api/data/', {'action':'requestPaths', 'userId': self.my_admin.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gamer.delete()


    def test_post_accessPath_none_accessed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        self.assertEqual(gamer.path.all().count(), 0)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'accessPath', 'userId': self.my_admin.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gamer.path.all().count(), 1)

        gamer.delete()

    def test_post_accessPath_access_accessed_path(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 1)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'accessPath', 'userId': self.my_admin.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gamer.path.all().count(), 1)

        gamer.delete()

    def test_post_accessPath_access_last_unaccessed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        pathLast = Path.objects.get(name="Path 5")

        for index in range(1, 4, 2):

            path = Path.objects.get(name="Path " + str(index))

            gamer.accessPath(path)

        self.assertEqual(gamer.path.all().count(), 2)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'accessPath', 'userId': self.my_admin.id, 'pathId': pathLast.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gamer.path.all().count(), 3)

        gamer.delete()

    def test_post_accessPath_routine(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        path = Path.objects.get(name="Path 3")

        self.assertEqual(gamer.path.all().count(), 1)
        
        response = self.client.post('/workoutgames/api/data/', {'action':'accessPath', 'userId': self.my_admin.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(gamer.path.all().count(), 2)

        gamer.delete()


    def test_post_completeWorkout_routine(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.filter(path=path)[0]

        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)
        
        self.assertEqual(pathInstance.workout.all().count(), 0)

        response = self.client.post('/workoutgames/api/data/', {'action':'completeWorkout', 'userId': self.my_admin.id, 'workoutId': workout.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pathInstance.workout.all().count(), 1)

        gamer.delete()
    
    def test_post_completeWorkout_complete_completed(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.filter(path=path, level=1)[0]

        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)

        gamer.completeWorkout(path, workout)
        
        self.assertEqual(pathInstance.workout.all().count(), 1)

        response = self.client.post('/workoutgames/api/data/', {'action':'completeWorkout', 'userId': self.my_admin.id, 'workoutId': workout.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pathInstance.workout.all().count(), 1)

        gamer.delete()

    def test_post_completeWorkout_higher_level(self):

        gamer = Gamer()
        gamer.user = self.my_admin
        gamer.save()

        path = Path.objects.get(name="Path 1")

        gamer.accessPath(path)

        workout = Workout.objects.filter(path=path, level=2)[0]

        pathInstance = PathInstance.objects.get(path=path, gamer=gamer)
        
        self.assertEqual(pathInstance.workout.all().count(), 0)

        response = self.client.post('/workoutgames/api/data/', {'action':'completeWorkout', 'userId': self.my_admin.id, 'workoutId': workout.id, 'pathId': path.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(pathInstance.workout.all().count(), 0)

        gamer.delete()


def imageWorkoutFactory(num, url, user, date=timezone.now(), isUpload=False):

    if not isUpload:

        signals.post_save.disconnect(extraSaveForImages, sender=ImageWorkout)
        signals.pre_delete.disconnect(image_delete_files, sender=ImageWorkout)

        for i in range(num):

            image = ImageWorkout()

            image.name = "test_image_" + str(i)
            image.added_by = user
            image.image_field.name = url
            image.date = date
            image.name = "This is a image test"
            image.thumbnail.name = url
            image.added_by = user
            image.save()

        signals.pre_delete.connect(image_delete_files, ImageWorkout)
        signals.post_save.connect(extraSaveForImages, ImageWorkout)


def videoWorkoutFactory(num, url, user, thumbnail=None, date=timezone.now(), isUpload=False):

    if not isUpload:
        
        signals.post_save.disconnect(extraSaveForVideos, sender=VideoWorkout)
        signals.pre_delete.disconnect(video_delete_files, sender=VideoWorkout)

        for i in range(num):

            video = VideoWorkout()

            video.name = "test_video_" + str(i)
            video.added_by = user
            video.video_field.name = url
            video.date = date
            video.name = "This is a video test"
            video.thumbnail.name = thumbnail
            video.added_by = user
            video.save()

        signals.pre_delete.connect(video_delete_files, VideoWorkout)
        signals.post_save.connect(extraSaveForVideos, VideoWorkout)

        


def workoutFactory(name, images, videos, tags, level=1, datePosted=timezone.now(), myId=None):

    workout = Workout()
    workout.name = name
    workout.datePosted = datePosted
    workout.level = level
    workout.slug = str(name)

    if myId != None:

        workout.id = myId
    
    workout.save()
    
    workout.tag.add(*tags)
    workout.image_content.add(*images)
    workout.video_content.add(*videos)

    workout.save()


def userFactory(password, username, email, district_name='Test', district_email='EmailTest', team_type='Green'):

    my_admin = User.objects.create_superuser(username, email, password)

    district = Districts()
    district.district = district_name
    district.emailDomain = district_email
    district.save()

    team = Teams()
    team.team = team_type
    team.district = district
    team.save()

    teacher = Teacher()
    teacher.user = my_admin
    teacher.team = team
    teacher.district = district
    teacher.save()

    return my_admin