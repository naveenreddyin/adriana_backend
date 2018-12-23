from rest_framework import serializers

from api.models import Topic


class ListALLTopicsSerializer(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True)

    class Meta:
        model = Topic
        fields = ('pk', 'text', 'parent', 'children')
