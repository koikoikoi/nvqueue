from rest_framework import serializers
from nvqueue.models import Printjob, Queue


class QueueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Queue
        fields = ('id', 'created', 'name', 'url', )
        fields = ('id', 'created', 'name', 'printjobs', 'url', )
        read_only_fields = ('printjobs',)


class PrintjobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Printjob
        fields = ('id', 'created', 'user', 'filename', 'printer', 'queue', 'state', 'url', )
