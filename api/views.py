import os
import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from api.serializers import ListALLTopicsSerializer, TopicLogSerializer, LoadSerializer
from api.models import Topic


class LoadJSONDataApiView(ListAPIView):
    """
    This will work as a util api to load the json file and display all the contents.
    The content will be stored in database.
    This could have been done using custom management command as well. 
    """
    queryset = Topic.objects.all()
    serializer_class = LoadSerializer

    def list(self, request):
        Topic.objects.all().delete()
        file_read = open(os.path.join(settings.BASE_DIR, settings.DATA_FILE))
        # deserialize it
        topics = json.load(file_read)

        # loop through data
        for topic in topics:
            if topic['parent_ref_id'] == None:
                Topic.objects.create(text=topic['text'], ref_id=topic['ref_id'])
            else:
                parent = Topic.objects.get(ref_id=topic['parent_ref_id'])
                Topic.objects.create(text=topic['text'], ref_id=topic['ref_id'], parent=parent)

        queryset = self.get_queryset()
        serializer = LoadSerializer(queryset, many=True)
        return Response(serializer.data)


class ListTopicsApiView(ListAPIView):
    """
    This api view is to show question and its children
    """
    queryset = Topic.objects.all()
    serializer_class = ListALLTopicsSerializer

    def list(self, request, parent_id=None, child_id=None):
        queryset = self.get_queryset()
        if not parent_id:
            queryset = queryset.filter(parent=None)
        else:
            parent = get_object_or_404(Topic, pk=parent_id)
            queryset = queryset.filter(parent=parent).filter(pk=child_id)

        serializer = ListALLTopicsSerializer(queryset, many=True)
        return Response(serializer.data)


class TopicLogCreateApiView(CreateAPIView):
    serializer_class = TopicLogSerializer
