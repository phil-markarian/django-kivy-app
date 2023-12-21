from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import TaskSerializer
from .serializers import StoreItemSerializer
from users.models import UserProfile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task, StoreItem

class AllTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Filter tasks based on the authenticated user
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            print(f"DEBUG: Successfully retrieved {len(tasks)} tasks.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"DEBUG: Error retrieving tasks - {str(e)}")
            return Response({"error": "Error retrieving tasks"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the task with the authenticated user
            serializer.validated_data['user'] = request.user
            serializer.save()
            tasks = Task.objects.filter(user=request.user)
            all_tasks_serializer = TaskSerializer(tasks, many=True)
            return Response(all_tasks_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreItemList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer

class StoreItemDetail(RetrieveUpdateDestroyAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            activated_item = serializer.instance
            user_profile.activated_items.add(activated_item)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': f'Failed to delete object. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


