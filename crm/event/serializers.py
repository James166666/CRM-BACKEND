from rest_framework import serializers
from event.models import Event

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'user', 'title', 'start', 'end']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event