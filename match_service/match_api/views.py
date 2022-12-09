from .serializers import MatchSerializer
from .models import Match
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class MatchViewSet(viewsets.ModelViewSet):

    serializer_class = MatchSerializer

    def get_object(self, pk):
        queryset = Match.objects.all()
        return get_object_or_404(queryset, pk=pk)

    # list
    def list(self, request):
        queryset = Match.objects.all()
        serializer_class = MatchSerializer(queryset, many=True)
        return Response(serializer_class.data)

    # get
    def get(self, request, pk=None):
        match = self.get_object(pk)
        serializer_output = MatchSerializer(match)
        return Response(serializer_output.data)

    # create
    def create(self, request):
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # update
    def update(self, request, pk):
        match = self.get_object(pk)
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid()
        serializer.update(match, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete
    def delete(self, request, pk):
        match = self.get_object(pk)
        match.delete()
        return Response(status=status.HTTP_200_OK)
        