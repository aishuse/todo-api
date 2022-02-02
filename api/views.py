from django.http import Http404
from django.shortcuts import render
from rest_framework import status

from api.models import Todo
from api.serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class Todos(APIView):
    model = Todo
    serializer_class = TodoSerializer
    def get(self,request):
        todos = self.model.objects.all()
        serializer = self.serializer_class(todos, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        else :
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TodoDetails(APIView):
    model = Todo
    serializer_class = TodoSerializer

    def get_object(self, pk):
        try:
            return self.model.objects.get(id=pk)
        except Todo.DOESNOTEXIST:
            raise Http404

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        todo = self.model.objects.get(id=id)
        serializer = self.serializer_class(todo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs ):
        id = kwargs['pk']
        todo = self.get_object(id)
        serializer = self.serializer_class(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,  request, *args, **kwargs):
        id = kwargs['pk']
        todo = self.get_object(id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

