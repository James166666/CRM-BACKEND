from rest_framework import serializers
from trello.models import Column, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'content', 'priority', 'column']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = f"task-{representation['id']}"
        return representation
    
    def create(self, validated_data):
        task = Task(
            content=validated_data['content'],
            priority=validated_data['priority'],
            column=validated_data['column']
        )
        task.save()
        return task

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # This will nest the cards within a column.

    class Meta:
        model = Column
        fields = ['id', 'user', 'title', 'tasks']  # 'cards' is added to show the related cards.
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = f"column-{representation['id']}"
        return representation


    def create(self, validated_data):
        # Extract tasks_data, default to an empty list if not present
        tasks_data = validated_data.pop('tasks', [])

        # Create the column instance
        column = Column.objects.create(**validated_data)

        # For each tasks_data, create a Card instance associated with the column
        for task_data in tasks_data:
            Task.objects.create(column=column, **task_data)

        return column