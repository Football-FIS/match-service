from .serializers import MatchSerializer
from .models import Match
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json

HOURS_TO_SEND_EMAIL = "HOURS_TO_SEND_EMAIL"
OPEN_WEATHER_KEY = "OPEN_WEATHER_KEY"
DEFAULT_OPEN_WEATHER_KEY = 'b8de83b3476d58590a4fbf3661f4dabe'
TEAM_SERV_URL = "TEAM_SERV_URL"

team_backend_url = os.getenv(TEAM_SERV_URL, 'http://localhost:8000/') + 'api/v1/'

def validate_token(headers):
    return requests.get(team_backend_url + 'validate-token', headers={'Authorization': headers['Authorization']})

def get_user_from_request(request):
    return json.loads(request.content)

def get_weather(city):
    open_weather_key = os.environ.get(OPEN_WEATHER_KEY, DEFAULT_OPEN_WEATHER_KEY)
    api = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key).json()
    if api['cod'] == '404':
        return ''
    celsius = api['main']['temp'] - 273.15
    return api['weather'][0]['description'] + ' - Temperatura: %.2f ' %celsius



class MatchViewSet(viewsets.ModelViewSet):

    serializer_class = MatchSerializer

    # list
    def list(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # list all matches from team
        # queryset = Match.objects.all()

        # list only from user
        user = get_user_from_request(bt)
        queryset = Match.objects.filter(user_id=user['id'])
        serializer_class = MatchSerializer(queryset, many=True)
        return Response(serializer_class.data)
        
    # get
    def get(self, request, pk=None):
        match = get_object_or_404(Match, pk=pk)
        serializer_output = MatchSerializer(match)
        return Response(serializer_output.data)

    #get url
    def get_url(self, request, pk=None):
        queryset = Match.objects.filter(url=pk)
        serializer_class = MatchSerializer(queryset, many=True)
        return Response(serializer_class.data)

    # create
    def create(self, request):

        # check permissions
        bt = validate_token(request.headers)
        if(bt.status_code!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # object to write
        match = request.data

        # WeatherAPI
        #match['weather'] = get_weather(request.data['city'])
            
        # Team service
        user = get_user_from_request(bt)
        match['user_id'] = user['id']

        serializer = MatchSerializer(data=match)
        if serializer.is_valid():
            serializer.validated_data['weather'] = get_weather(request.data['city'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


    # update
    def update(self, request,pk):

        # object to write
        new_match = request.data

        # get saved match
        match = get_object_or_404(Match, id=pk)

        # check permissions
        '''bt = validate_token(request.headers)
        user = get_user_from_request(bt)
        if(bt.status_code!=200 and match.user_id == user['id']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)'''

        # WeatherAPI
        #new_match['weather'] = get_weather(request.data['city'])
            
        # Team service
        '''user = get_user_from_request(bt)
        new_match['user_id'] = user['id']'''

        # update if valid
        serializer = MatchSerializer(match,data=request.data)
        '''serializer.is_valid()
        serializer.update(match, new_match)
        return Response(serializer.data, status=status.HTTP_200_OK)'''
        if serializer.is_valid():
            serializer.validated_data['weather'] = get_weather(request.data['city'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        

    # delete
    def delete(self, request, pk):

        # get saved match
        match = get_object_or_404(Match, pk=pk)

        # check permissions
        bt = validate_token(request.headers)
        user = get_user_from_request(bt)
        if(bt.status_code!=200 and match.user_id == user['id']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # delete
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendEmailSet(viewsets.ModelViewSet):

    serializer_class = MatchSerializer

    # get
    def get_request(self, pk):

        # filter by date (given by environment variable)
        hours_to_send_email = int(os.environ.get(HOURS_TO_SEND_EMAIL, '3'))
        date = datetime.now() - relativedelta(hours=hours_to_send_email)
        matches = Match.objects.filter(sent_email = True, start_date_lte = date)

        for match in matches:

            # update weather
            match['weather'] = get_weather(match['city'])

            # send to backend
            requests.post(team_backend_url + 'send-email-player', data=match)

            # updated with sent_email
            modified_match = match
            modified_match.sent_email = True
            serializer = MatchSerializer(data=match)
            serializer.update(match, modified_match)

        # return HTTP 200
        return Response(data=None, status=status.HTTP_200_OK)
