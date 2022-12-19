from .serializers import MatchSerializer
from .models import Match
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests

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
        openWeatherKey ='b8de83b3476d58590a4fbf3661f4dabe'

        serializer = MatchSerializer(data=request.data)

        city = request.data['city']
        api = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + openWeatherKey).json()
        #celsius = (api['main']['temp'] - 32) / 1.8
        
        if api['cod'] == '404':
            return Response(status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():

            celsius = api['main']['temp'] - 273.15
            
            serializer.validated_data['weather'] = api['weather'][0]['description'] + ' - Temperatura: %.2f ' %celsius
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


        

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
        return Response(status=status.HTTP_204_NO_CONTENT)
        