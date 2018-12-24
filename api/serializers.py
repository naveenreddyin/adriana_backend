from rest_framework import serializers

from api.models import Topic, TopicLog


class TopicRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Topic.objects.all()
    def to_representation(self, value):
        count = Topic.objects.filter(parent=value.pk).count()
        return {'pk': value.pk, 'text': value.text, 'count': count}


class ListALLTopicsSerializer(serializers.ModelSerializer):
    children = TopicRelatedField(read_only=True, many=True)

    class Meta:
        model = Topic
        fields = ('pk', 'text', 'parent', 'children')


class TopicLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicLog
        fields = ('__all__')

