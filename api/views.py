import os
import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.serializers import ListALLTopicsSerializer
from api.models import Topic


class LoadJSONDataApiView(ListAPIView):
    """
    This will work as a util api to load the json file and display all the contents.
    The content will be stored in database.
    This could have been done using custom management command as well. 
    """
    queryset = Topic.objects.all()
    serializer_class = ListALLTopicsSerializer

    def list(self, request):
        file_read = open(os.path.join(settings.BASE_DIR, settings.DATA_FILE))
        # deserialize it
        topics = json.load(file_read)
        
        # loop through data
        for topic in topics:
            parent = None
            # Check if text exists if not create and that is considered parent
            if Topic.objects.filter(text=topic['text']).count() == 0:
                parent = Topic.objects.create(text=topic['text'])
            else:
                parent = Topic.objects.get(text=topic['text'])
                
            # check for children, iterate and create new nodes
            for text in topic['children']:
                Topic.objects.create(text=text, parent=parent)

        queryset = self.get_queryset()
        serializer = ListALLTopicsSerializer(queryset, many=True)
        return Response(serializer.data)


class ListTopicsApiView(ListAPIView):
    """
    This api view is to show question and its children
    """
    queryset = Topic.objects.all()
    serializer_class = ListALLTopicsSerializer

    def list(self, request, parent_id=None, text=None):
        queryset = self.get_queryset()

        if not parent_id:
            queryset = queryset.filter(parent=None)
        else:
            parent = get_object_or_404(Topic, pk=parent_id)
            queryset = queryset.filter(parent=parent).filter(text__iexact=text)

        serializer = ListALLTopicsSerializer(queryset, many=True)
        return Response(serializer.data)
