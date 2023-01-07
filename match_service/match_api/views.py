from .serializers import MatchSerializer
from .models import Match
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

HOURS_TO_SEND_EMAIL = "HOURS_TO_SEND_EMAIL"
OPEN_WEATHER_KEY = "OPEN_WEATHER_KEY"
DEFAULT_OPEN_WEATHER_KEY = 'b8de83b3476d58590a4fbf3661f4dabe'
TEAM_SERV_URL = "TEAM_SERV_URL"

team_backend_url = os.getenv(TEAM_SERV_URL, 'https://team-service-danaremar.cloud.okteto.net/api/v1/')

def validate_token(headers):
    return requests.post(team_backend_url + ' validate-token', headers=headers)

class MatchViewSet(viewsets.ModelViewSet):

    serializer_class = MatchSerializer

    # list
    def list(self, request):

        # check permissions
        bt = validate_token(self.headers)
        if(bt['cod']!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        # list all matches from team
        # queryset = Match.objects.all()
        queryset = Match.objects.filter(user_uid=bt['pk'])
        serializer_class = MatchSerializer(queryset, many=True)
        return Response(serializer_class.data)
        
    # get
    def get(self, request, pk=None):
        match = self.get_object(pk)
        serializer_output = MatchSerializer(match)
        return Response(serializer_output.data)

    # create
    def create(self, request):

        # check permissions
        bt = validate_token(self.headers)
        if(bt['cod']!=200):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        open_weather_key = os.environ.get(OPEN_WEATHER_KEY, DEFAULT_OPEN_WEATHER_KEY)

        serializer = MatchSerializer(data=request.data)

        city = request.data['city']
        api = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key).json()
        
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

        # get saved match
        match = self.get_object(pk)

        # check permissions
        bt = validate_token(self.headers)
        if(bt['cod']!=200 and match.user_uid == bt['pk']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # update if valid
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid()
        serializer.update(match, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete
    def delete(self, request, pk):
        # get saved match
        match = self.get_object(pk)

        # check permissions
        bt = validate_token(self.headers)
        if(bt['cod']!=200 and match.user_uid == bt['pk']):
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
            # TODO: send to TeamService
            requests.post(team_backend_url + 'send-email-player', data=match)

            # updated with sent_email
            modified_match = match
            modified_match.sent_email = True
            serializer = MatchSerializer(data=match)
            serializer.update(match, modified_match)

        # return HTTP 200
        return Response(data=None, status=status.HTTP_200_OK)
