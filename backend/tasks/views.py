from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskInputSerializer
from .scoring import score_tasks


class AnalyzeTasks(APIView):
    """
    POST /api/tasks/analyze/
    Accepts a list of tasks and returns them sorted by score
    """

    def post(self, request):
        tasks = request.data

        if not isinstance(tasks, list):
            return Response({"error": "Input must be a list of tasks"}, status=400)

        serializer = TaskInputSerializer(data=tasks, many=True)
        serializer.is_valid(raise_exception=True)

        mode = request.query_params.get("mode", "smart")

        scored = score_tasks(serializer.validated_data, mode=mode)
        return Response({"tasks": scored}, status=200)


class SuggestTasks(APIView):
    """
    GET /api/tasks/suggest/
    Returns top 3 tasks with explanations
    """

    def post(self, request):
        tasks = request.data

        if not isinstance(tasks, list):
            return Response({"error": "Input must be a list of tasks"}, status=400)

        serializer = TaskInputSerializer(data=tasks, many=True)
        serializer.is_valid(raise_exception=True)

        mode = request.query_params.get("mode", "smart")

        scored = score_tasks(serializer.validated_data, mode=mode)
        top3 = scored[:3]

        return Response({"suggestions": top3}, status=200)
