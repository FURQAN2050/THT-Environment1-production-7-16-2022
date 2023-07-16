from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.utils import html
from django.utils import timezone
from django.db.models import Q

import json

from ..models import Workout, Path, PathInstance, Gamer, WorkoutPlace, Movement, MovementInstance, Set
from accounts.models import User


class WorkoutAPI(APIView):

    """
    API returns data about paths and workouts
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print("heere")

    def post(self, request):


        user = request.user

        if len(Gamer.objects.filter(user=user)) <= 0:

            if len(User.objects.filter(id=user.id)) <= 0:
            
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                self.createGamer(user)

        if request.POST['action'] == 'requestWorkoutOpen':
            
            return Response(
                self.requestWorkoutOpen(
                    request.POST['workoutId'], 
                    user, 
                    request.POST['pathId']
                )
            )

        if request.POST['action'] == 'requestWorkoutList':
            
            return Response(
                self.requestWorkoutList(
                    request.POST['pathId'],
                    user
                )
            )

        if request.POST['action'] == 'requestPaths':

            print("it goes here")

            return Response(
                self.requestPaths(
                    user
                )
            )

        if request.POST['action'] == 'accessPath':

            return Response(
                self.accessPath(
                    user,
                    request.POST['pathId']
                )
            )

        if request.POST['action'] == 'completeWorkout':

            return Response(
                self.completeWorkout(
                    user,
                    request.POST['workoutId'],
                    request.POST['pathId']
                )
            )

        if request.POST['action'] == 'requestMovementsList':

            return Response(
                self.requestMovementsList(
                    request.POST['workout'],
                    request.POST['path_instance_id'],
                    request.POST['location'],
                )
            )

        if request.POST['action'] == 'completeSet':
            
            return Response(
                self.completeSet(
                    int(request.POST['reps']),
                    int(request.POST['weight']),
                    int(request.POST['set']),
                    request.POST['movement_id'],
                    request.POST['path_instance_id']
                )
            )

        if request.POST['action'] == 'requestMovementHistory':

            return Response(
                self.requestMovementsHistory(
                    request.POST['id'],
                    request.POST['pathInstanceId']
                )
            )

        if request.POST['action'] == 'requestWorkoutOfTheDay':

            return Response(
                self.getWorkoutOfTheDay(
                    user
                )
            )

        else:

            print("WHAT?")
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def requestWorkoutOpen(self, workoutId, user, pathId):

        """
        Gets a workout's name, description, and media
        
        Post:
            Returns information if gamer can access workout or
            returns Null for all values if gamer cannot access
            workout

        Parameters: 
            workoutId(Integer): Workout id to get
            user(User): Current user
            pathId(Integer): Path id from workout

          
        Returns: 
            Dictionary: Dictionary with name, description, and media
        """

        data = dict()
        
        try:
            workout = Workout.objects.get(id=workoutId)
            path = Path.objects.get(id=pathId, workout__in=[workout])
            pathInstance = PathInstance.objects.get(gamer__in=[user.gamer], path=path)
            
        except Exception as err:
            raise Exception(err)

        
        if path.canUserAccessWorkout(user.gamer, workout):

            data = {"id": workout.id,
                    "name" : workout.name,
                    "description" : html.linebreaks(html.escape(html.mark_safe(workout.description))),
                    "datePosted" : workout.datePosted,
                    "level" : workout.level,
                    "tag" : [str(tag) for tag in workout.tag.all()],
                    "completed" : pathInstance.isWorkoutComplete(workout),
                    "image_content" : [str(w.image_field.url) for w in workout.image_content.all()],
                    "image_titles" : [str(w.name) for w in workout.image_content.all()],
                    "video_content" : [str(w.video_field.url) for w in workout.video_content.all()],
                    "video_titles" : [str(w.name) for w in workout.video_content.all()],
                    "video_content_thumbnails" : [str(w.thumbnail.url) for w in workout.video_content.all()],
            }

        else:

            data = {"id": None,
                    "name" : None,
                    "description" : None,
                    "datePosted" : None,
                    "level" : None,
                    "tag" : None,
                    "image_content" : None,
                    "image_title" : None,
                    "video_content" : None,
                    "video_title" : None}

        return data

            


    def requestWorkoutList(self, pathId, user):

        """
        Gets a list of workout with their name, thumbnail, level, path,
        and completion status

        Parameters: 
            pathId(Integer): Path's id to get workouts from
            user(User): Current user

          
        Returns: 
            Dictionary: Dictionary with name, thumbnail url, level, path,
            and completion status
        """

        data = dict()
        
        try:
            path = Path.objects.get(id=pathId)
            
        except Exception as err:
            raise Exception(err)

        workouts = Workout.objects.filter(path__in=[path]).order_by('level', 'name')

        if not user.gamer.isPathAccessed(path):
            user.gamer.accessPath(path)

        path_instance = PathInstance.objects.filter(gamer__in=[user.gamer]).filter(path__in=[path])
        if len(path_instance) > 0:

            print([workout.id for workout in workouts])
        
            data = {
                    "id" : [workout.id for workout in workouts],
                    "name" : [workout.name for workout in workouts],
                    "description" : [workout.description for workout in workouts],
                    "datePosted" : [workout.datePosted for workout in workouts],
                    "level" : [workout.level for workout in workouts],
                    "tag" : [workout.tag.all().values_list('workout') for workout in workouts],
                    "thumbnail" : [str(workout.getThumbnail()) for workout in workouts],
                    "accessible" : ("Yes" if path.canUserAccessWorkout(user.gamer, workout) 
                                else "No" 
                                for workout in workouts),
                    "completed" : ("Yes" if user.gamer.isWorkoutComplete(path, workout) 
                                else "No" 
                                for workout in workouts),
                    "path_instance_id": path_instance[0].id,
                }

        else:

            data = {
                    "id": None,
                    "name" : None,
                    "description" : None,
                    "datePosted" : None,
                    "level" : None,
                    "tag" : None,
                    "thumbnail" : None,
                    "completed" : None,
                    "path_instance_id": None
                }


            print(data)

        return data
        

    def requestPaths(self, user):

        """
        Gets a list of paths with their name, description, and access
        status from gamer

        Parameters: 
            user(User): Current user
          
        Returns: 
            Dictionary: Dictionary with name, description, and access
            status from user
        """

        data = dict()

        paths = Path.objects.order_by('levelPath')
        
        data = {"id" : [path.id for path in paths],
                "name" : [path.name for path in paths],
                "description" : [path.description for path in paths],
                "workouts" : [path.workout.all().count() for path in paths],
                "accessed" : [user.gamer.isPathAccessed(path) for path in paths],
                "accessible" : ("Yes" if (path.canUserAccessPath(user.gamer))# and user.gamer.checkAccessedPath(path))
                                else "No" 
                                for path in paths),
                "thumbnail" : [path.getThumbnail() for path in paths],
                "workoutsCompleted": (PathInstance.objects.get(
                                                gamer__in=[user.gamer], 
                                                path__in=[path]).workout.all().count() 
                                            if user.gamer.isPathAccessed(path) 
                                            else 0 
                                        for path in paths),
                "currentLevel" : (PathInstance.objects.get(
                                                gamer__in=[user.gamer], 
                                                path__in=[path]).currentLevel 
                                            if user.gamer.isPathAccessed(path) 
                                            else 0 
                                        for path in paths)}

        return data

    def accessPath(self, user, pathId):

        """
        Allows user to access a path and updates models

        Post:
            p = new PathInstance where PathInstance.path = findPath(pathId)
            findUser(userId).path = #findUser(userId).path o <p>

        Parameters: 
            pathId(Integer): Path's Id to get workouts from
            user(User): Current user

          
        Returns: 
            Dictionary: Dictionary with success status
        """

        data = dict()

        try:
            path = Path.objects.get(id=pathId)

        except Exception as err:
            raise Exception(err)
            return status.HTTP_400_BAD_REQUEST

        if user.gamer.accessPath(path):
            data = {"accessed" : True}

        else:
            data = {"accessed" : False}

        return data


    def requestMovementsList(self, workout_place_id, pathinstance_id, location):

        """
        Gets a list of movements with all their data

        Parameters: 
            workoutId(Integer): Workout's id to get movements from
            user(User): Current user
            pathinstance_id(Integer): Id of a path instance
          
        Returns: 
            Dictionary
        """

        data = dict()
        
        try:
            workout = Workout.objects.get(id=workout_place_id)
            workout_place = WorkoutPlace.objects.get(Q(workout=workout, place='B') | Q(workout=workout, place=location))
            path_instance = PathInstance.objects.get(id=pathinstance_id)
            
        except Exception as err:
            raise Exception(err)

        movements = Movement.objects.filter(workoutplace__in=[workout_place]).order_by('order')

        print("Workout Place Id: " + str(workout_place.id))

        data = {
            "workout_place_id" : workout_place.id,
            "id" : [movement.id for movement in movements],
            "type_id" : [movement.movement_type.id for movement in movements],
            "names" : [movement.movement_type.name for movement in movements],
            "rec_sets" : [movement.base_sets for movement in movements],
            "rec_reps" : [movement.base_reps for movement in movements],
            "rec_weight" : [movement.base_weight for movement in movements],
            "videos" : [movement.movement_type.video_content for movement in movements],
            "circuits" : [movement.circuit for movement in movements],
        }

        data['sets_completed'] = []

        for movement in movements:

            movement_instance = MovementInstance.objects.filter(movement=movement, path_instance=path_instance)

            if len(list(movement_instance)) <= 0:
                movement_instance = MovementInstance(
                    movement=movement,
                    path_instance=path_instance,
                    recommended_reps=movement.base_reps,
                    recommended_sets=movement.base_sets,
                    recommended_weight=movement.base_weight,
                )

            else:
                movement_instance = list(movement_instance)[0]

            data['sets_completed'].append(movement_instance.completed_sets)

        return data



    def createGamer(self, user):

        gamer = Gamer(user=user)
        gamer.save()



    def completeSet(self, reps, weight, set_num, movement_id, path_instance_id):

        """
        Records a completed set

        Parameters:
            reps(Integer) - Number of repetitions
            weight(Float) - Weight
            set(Integer) - Number of completed set
            movement_id(Integer) - ID of movement
        
        Returns:
            Dictionary
        """

        movement = Movement.objects.get(id=movement_id)
        path_instance = PathInstance.objects.get(id=path_instance_id)
        movement_instance = MovementInstance.objects.filter(movement=movement, path_instance=path_instance)

        if len(list(movement_instance)) <= 0:
            movement_instance = MovementInstance(
                movement=movement,
                path_instance=path_instance,
                recommended_reps=movement.base_reps,
                recommended_sets=movement.base_sets,
                recommended_weight=movement.base_weight,
            )

        else:
            movement_instance = list(movement_instance)[0]

        if movement_instance.completed_sets < movement.base_sets:

            movement_instance.date_completed = timezone.now()
            movement_instance.completed_sets += 1
            movement_instance.save()

            my_set = Set(
                completed_reps=reps,
                set_num=set_num,
                used_weight=weight,
                date_completed=timezone.now(),
                movement_instance=movement_instance
            )

            my_set.save()

        data = {
            "id" : movement.id,
            "completed_sets" : movement_instance.completed_sets,
        }

        return data




    def completeWorkout(self, user, workoutId, pathId):

        """
        Allows user to complete workout and updates models

        Pre:
            user.path contains pathInstance where pathInstancen.path = findPathInstance(user, pathId)

        Post:
            findPathInstance(userId, pathId) = #findPathInstance(user, pathId) o <findWorkout(workoutId)>

        Parameters:
            pathId(Integer): Path's Id to get workouts from
            user(User): Current user
            workoutId(Integer): Workout to complete

          
        Returns: 
            Dictionary: Dictionary with success status
        """

        data = dict()

        try:
            path = Path.objects.get(id=pathId)
            pathInstance = PathInstance.objects.get(path__in=[path], gamer__in=[user.gamer])

        except Exception as err:

            raise Exception(err)
            return status.HTTP_400_BAD_REQUEST

        try:

            workout = Workout.objects.get(id=workoutId)

        except Exception as err:

            raise Exception(err)
            return status.HTTP_400_BAD_REQUEST

        if user.gamer.completeWorkout(path, workout):
        
            data = {"completed" : True}

        else:

            data = {"completed" : False}

        return data


    def requestMovementsHistory(self, workout_place_id, path_instance_id):

        """
        Obtains movement type history from the database

        Parameters:
            movement_id(Integer)

        Returns:
            Dictionary:
                Date(List)
                Sets(List)
                Reps(List)
                Weight(List)
        """

        data = dict()

        workout_place = WorkoutPlace.objects.get(id = workout_place_id)
        movement = workout_place.movements.all()
        movement_type = [ind_movement.movement_type for ind_movement in list(movement)]
        movements = Movement.objects.filter(movement_type__in=movement_type)
        movement_instances = MovementInstance.objects.filter(movement__in=list(movements), path_instance__id=path_instance_id)

        sets = Set.objects.filter(movement_instance__in=list(movement_instances)).order_by('-date_completed')

        # completed_dates = set([(i.date_completed.year, i.date_completed.month, i.date_completed.day) for i in sets])
        # sets_separated = dict([(' '.join([str(number) for number in d]), []) for d in completed_dates])
        
        # for d in completed_dates:
        #     for i in sets:
        #         if (i.date_completed.year, i.date_completed.month, i.date_completed.day) == d:
        #             sets_separated[' '.join([str(number) for number in d])].append(i)

        
        data = {
            'movement_id' : [my_set.movement_instance.movement.movement_type.id for my_set in sets],
            'completed_dates' : [my_set.date_completed.date() for my_set in sets],
            'set_num' : [my_set.set_num for my_set in sets],
            'reps' : [my_set.completed_reps for my_set in sets],
            'weight': [my_set.used_weight for my_set in sets],
        }

        return data



    def getWorkoutOfTheDay(self, user):

        """
        Function returns the lowest level workout that has not been completed by the
        user

        Parameters:
            user(User): User requesting

        Returns
            Dictionary: Containing
                id(Integer)
                name(String)
                description(String)
                thumbnail(String)

        """
        data = {}
        next_workout = None
        gamer = user.gamer
        path = gamer.accessedPath

        if path != None:

            pathinstance = PathInstance.objects.filter(gamer__in=[gamer], path=path).order_by('-dateStarted')
            pathinstance = list(pathinstance)[0]

            workouts_in_path = path.workout.all()
            workouts_completed = pathinstance.workout.all()
            workouts_to_complete = workouts_in_path.exclude(id__in=[workout.id for workout in workouts_completed])

            workouts_to_complete = workouts_to_complete.order_by('level')
            
            if len(list(workouts_to_complete)) > 0:
                next_workout = workouts_to_complete[0]

        if next_workout != None:

            data = {
                'id': next_workout.id,
                'pathid': path.id,
                'name': next_workout.name,
                'description': next_workout.description,
            }

        else:

            data = {
                'id': None,
                'pathid': None,
                'name': None,
                'description': None,
            }

        return data


