from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task

class AllTasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTaskView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tasks = Task.objects.all()  # Retrieve all tasks after creation
            all_tasks_serializer = TaskSerializer(tasks, many=True)
            return Response(all_tasks_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
