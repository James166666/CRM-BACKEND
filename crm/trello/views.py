from django.shortcuts import render
from .serializers import ColumnSerializer, TaskSerializer
from .models import Column, Task


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class ColumnCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # sample url: http://127.0.0.1:8000/trello/column/?str=column-1
    # use string get specific column
    # OR
    # sample url: http://127.0.0.1:8000/trello/column/
    # get all of the user's column
    def get(self, request):
    # Check if column_id query parameter is provided
        column_id_str = request.query_params.get('str')
        if column_id_str and column_id_str.startswith("column-"):
            column_id = int(column_id_str.split("-")[1])
        else:
            column_id = None

        if column_id:
            try:
                # Ensure column exists
                column = Column.objects.get(id=column_id)
                # Check if the column belongs to the authenticated user
                if column.user != request.user:
                    return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            
                # Get all tasks for the column
                serializer = ColumnSerializer(column)
                return Response(serializer.data)
            except Column.DoesNotExist:
                return Response({'error': 'Column not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no column_id is provided, return all columns for the user
            columns = Column.objects.filter(user=request.user)
            serializer = ColumnSerializer(columns, many=True)
            return Response(serializer.data)
    

    def post(self, request):
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# List and Create
class TaskCreateView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # sample url: http://127.0.0.1:8000/trello/task/?str=column-1
    # use string get belonging tasks
    # OR
    # sample url: http://127.0.0.1:8000/trello/task/?str=task-1
    # use string get specific task
    def get(self, request):

        column_id_str = request.query_params.get('str')
        if column_id_str and column_id_str.startswith("column-"):
            column_id = int(column_id_str.split("-")[1])
        else:
            column_id = None

        if column_id_str and column_id_str.startswith("task-"):
            task_id = int(column_id_str.split("-")[1])
        else:
            task_id = None

        # if not column_id:
        #     return Response({"error": "column_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if column_id:
            try:
                column = Column.objects.get(id=column_id)
            except Column.DoesNotExist:
                return Response({'error': 'Column not found'}, status=status.HTTP_404_NOT_FOUND)

            tasks = Task.objects.filter(column=column)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        elif task_id:
            task = Task.objects.get(id=task_id)
            if task is None:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        task_id_str = request.query_params.get('str')
        if task_id_str and task_id_str.startswith("task-"):
            task_id = int(task_id_str.split("-")[1])
        else:
            task_id = None

        if task_id is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        task_id_str = request.query_params.get('str')
        if task_id_str and task_id_str.startswith("task-"):
            task_id = int(task_id_str.split("-")[1])
        else:
            task_id = None

        if task_id is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



