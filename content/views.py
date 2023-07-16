from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.utils import html
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tag
from .models import Content


class ContentViewPage(generic.CreateView):

    def get(self, request):

        user = request.user

        if user.teacher.processingSubscription:
            return render(request, "subscriptionProcessing.html")

        if not user.teacher.isSubscriptionGood():
            return redirect('/accounts/subscribe/')

        if user.teacher.team == None:
            return redirect('/accounts/finish/')

        # Ensure user only sees this page if it has not completed it before

        if user.teacher.gender == None:
            return redirect('/accounts/healthinfo')

        return render(request, 'content.html')


class ContentView(APIView):

    """
    API to return content information
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    datesSent = []

    def post(self, request):

        for key, value in request.session.items():

            print(key, ",", value)

        user = request.user

        if request.POST['action'] == 'getContent':
            
            return Response(
                self.getContent(
                    request.POST['tags'],
                    int(request.POST['length']),
                    timezone.now() if request.POST['startDate'] == "now" else request.POST['startDate']
                )
                )

        if request.POST['action'] == 'getContentOpen':

            return Response(
                self.getContentOpen(
                    request.POST['id']
                )
            )
        
        return Response()

    # Get content objects from database

    def getContent(self, tags, length, startDate):

        """ Gets content objects from database
        
        Parameters:
            tags(Tag[0...*]): Content keywords
            startDate(Date): Period to start. Use "now" for current time
            length(Integer): Number of elements to get

        Returns:
            Content[0...length]: Content associated with tags beginning on startDate

        """

        objects = Content.objects.filter(datePosted__lt=startDate).order_by('sortOrder')

        objects = objects[:length]

        print(len(objects))

        data = {
            "names": [o.name for o in objects],
            "id": [o.id for o in objects],
            "datesPosted": [o.datePosted for o in objects],
            "tags": [o.tags.all().values_list('element') for o in objects],
            "thumbnail": [str(o.getThumbnail()) for o in objects],
            "description": [o.description for o in objects],
        }

        return data

    def getContentOpen(self, id):

        """ Gets content objects from database
        
        Parameters:
            id(Integer): Id of element to return

        Returns:
            Dict: Keys -> Values U {e}
            Dict(x) =
                object.name if x = "name"
                object.id if x = "id"
                object.description if x = "description"
                object.datePosted if x = "datePosted"
                {x | x E object.videos} if x = "videos"
                {x | x E object.images} if x = "images"
                {x | x E object.videos.thumbnail} if x = "videosThumbnail"
                {x | x E object.images.thumbnail} if x = "imagesThumbnail"
                {x | x E object.tags} if x = "tags"

        """

        element = Content.objects.get(id = id)

        data = {
            "names": element.name,
            "id": element.id,
            "datePosted": element.datePosted,
            "videosThumbnail": [str(e.get_thumbnail()) for e in element.video_content.all()],
            "videosNames": [str(e.name) for e in element.video_content.all()],
            "imagesThumbnail": [str(e.thumbnail.url) for e in element.image_content.all()],
            "imagesNames": [str(e.name) for e in element.image_content.all()],
            "videos": [str(e.video_field) for e in element.video_content.all()],
            "images": [str(e.image_field.url) for e in element.image_content.all()],
            "docs": [str(e.doc_field.url) for e in element.doc_content.all()],
            "docsNames": [str(e.name) for e in element.doc_content.all()],
            "tags": element.tags.all().values_list('element'),
            "description": html.linebreaks(html.escape(html.mark_safe(element.description))),
        }

        return data

class SearchView(APIView):

    """
    API to return content elements based on queries
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.GET['action'] == "filterContent":

            return Response(
                self.get_queryset_content(
                    request.GET['query']
                )
            )

    def get_queryset_content(self, query):

        """ 
        Searches content objects in database that match query
        
        Parameters:
            query(String): String to search by. If first character equals '#'
                search will be based on Tag objects

        Returns:
            Dict: Keys -> Values U {e}
            Dict(x) =
                {x | x if x.name = query or (x if anyOf(x.tags) = query and query[0] = '#')}


        """

        if len(query) == 0:
            return None

        if query[0] == '#':

            query = query[1:]

            tag = Tag.objects.get(
                Q(element=query)
            )

            if(tag != None):
                query_result = tag.content_set.all()

            else:
                query_result = None

        else:

            query_result = Content.objects.filter(
                Q(name__icontains=query)
            )

        data = {
            'name' : [element.name for element in query_result],
            'id' : [element.id for element in query_result],
            'tags' : [element.tags.all().values_list('element') for element in query_result],
        }

        return data






