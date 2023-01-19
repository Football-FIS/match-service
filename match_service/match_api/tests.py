from django.db import connections
from django.db.utils import OperationalError
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework.response import Response
from .models import Match
from .views import MatchViewSet, SendEmailSet
from .serializers import MatchSerializer
import os
import requests
import pytest
# Create your tests here.


team_url = 'https://team-service-danaremar.cloud.okteto.net/api/v1/'

def mock_create(datos):
            serializador = MatchSerializer(data=datos)
            if serializador.is_valid():
                serializador.validated_data['weather'] = 'clear sky'
                #serializador.validated_data['weather'] = get_weather(datos['city'])
                serializador.save()
                return Response(serializador.data, status=201)
            else:
                return Response(serializador.data, status=400)

def mock_update(obj,datos):
            

            serializador = MatchSerializer(obj,data=datos,partial=True)
            print('------------serializador-------------')
            print(serializador)
            if serializador.is_valid():
                serializador.validated_data['weather'] = 'clear sky'
                serializador.save()
                return Response(serializador.data, status=200)
            else:
                #print('------------serializador-------------')
                #print(serializador.errors)
                #print(serializador.data)
                return Response(serializador.data, status=400)

class TestCreate(TestCase):

    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match.
    """
    @pytest.mark.django_db
    def test_create_match(self):

        json_match = {
                    'user_id' :2,
                    'opponent' : 'Sevilla',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        
        request_url = '/api/v1/match/'

        MatchViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchViewSet.create(json_match)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 201

    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with city more 50 characters
    """
    
    @pytest.mark.django_db
    def test_create_city_error(self):

        json_match = {
                    'user_id' :2,
                    'opponent' : 'Barcelona',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :get_random_string(length=55),
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        

        MatchViewSet.create = mock_create
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400
            
    """
        Check create method in Match with aligment more 250 characters
    """
    @pytest.mark.django_db
    def test_create_aligment_error(self):

        json_match = {
                    'user_id' :2,
                    'opponent' : 'Barcelona',
                    'is_local' : True,
                    'alignment' : get_random_string(length=260),
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :'barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        

        MatchViewSet.create = mock_create
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400
            
    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with opponent more 250 characters
    """
    

    @pytest.mark.django_db
    def test_create_opp_error(self):

        json_match = {
                    'user_id' :2,
                    'opponent' : get_random_string(length=260),
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        

        MatchViewSet.create = mock_create
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400
    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with opponent blank
    """ 
    @pytest.mark.django_db
    def test_create_match_opponent_blank(self):

        
        json_match = {
                    'user_id' :2,
                    'opponent' : '',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        
        request_url = '/api/v1/match/'

        MatchViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchViewSet.create(json_match)
        print('-----------Response------------------')
        print(response.data)
        assert response.status_code == 400
    
    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with date blank
    """ 
    @pytest.mark.django_db
    def test_create_match_date_blank(self):

        
        json_match = {
                    'user_id' :2,
                    'opponent' : 'Sevilla',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hl',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '',
                    'sent_email' : False
                }
        
        request_url = '/api/v1/match/'

        MatchViewSet.create = mock_create
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400


    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with url blank
    """ 
    @pytest.mark.django_db
    def test_create_match_url_blank(self):

        
        json_match = {
                    'user_id' :2,
                    'opponent' : '',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': '',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        
        request_url = '/api/v1/match/'

        MatchViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400

    """
        COMPONENT / DB INTEGRATION TEST:
        Check create method in Match with url more than 50 characters
    """ 
    @pytest.mark.django_db
    def test_create_match_url_error(self):

        
        json_match = {
                    'user_id' :2,
                    'opponent' : '',
                    'is_local' : True,
                    'alignment' : '4-3-3',
                    'url': 'https://www.google.com/webhp?hlasdafefedsdascacwac/adasfacascasdfascasc',
                    'city' :'Barcelona',
                    'weather' : 'clouds',
                    'start_date' : '2023-01-11T13:38:00Z',
                    'sent_email' : False
                }
        
        request_url = '/api/v1/match/'

        MatchViewSet.create = mock_create
        #response = client.post(request_url, data=json_match, format='json')
        response = MatchViewSet.create(json_match)
        
        assert response.status_code == 400


    """
        COMPONENT / DB INTEGRATION TEST:
        Check update method in Match.
    """
    @pytest.mark.django_db
    def test_update_match(self):

        
        """
        Check update method in match.
        """

        objeto = Match.objects.create(
            user_id = 6,
            opponent = 'Sevilla',
            is_local = True,
            alignment ='4-3-3',
            url= 'https://www.google.com/webhp',
            city ='Barcelona',
            weather = 'clear',
            start_date = '2023-01-11T13:38:00Z',
            sent_email = False
        )

        json_match = {
            'id':objeto.id,
            'user_id' : 6,
            'opponent' : 'Sevilla',
            'is_local' : True,
            'alignment' : '4-2-1',
            'url': 'https://www.google.com/webhp',
            'city' :'Caracas',
            'weather' : 'clear',
            'start_date' : '2023-01-11T13:38:00Z',
            'sent_email' : False
            
        }

        
        MatchViewSet.update = mock_update
        match_obj = Match.objects.get(id=objeto.id)
        print(match_obj)
        response = MatchViewSet.update(objeto,json_match)


        assert response.status_code == 200


    """
        COMPONENT / DB INTEGRATION TEST:
        Check update method in Match with opponent blank
    """
    @pytest.mark.django_db
    def test_update_match_opp_blank(self):

        
        """
        Check update method in match.
        """

        objeto = Match.objects.create(
            user_id = 6,
            opponent = 'Sevilla',
            is_local = True,
            alignment ='4-3-3',
            url= 'https://www.google.com/webhp',
            city ='Barcelona',
            weather = 'clear',
            start_date = '2023-01-11T13:38:00Z',
            sent_email = False
        )

        json_match = {
            'id':objeto.id,
            'user_id' : 6,
            'opponent' : '',
            'is_local' : True,
            'alignment' : '4-2-1',
            'url': 'https://www.google.com/webhp',
            'city' :'Caracas',
            'weather' : 'clear',
            'start_date' : '2023-01-11T13:38:00Z',
            'sent_email' : False
            
        }

        
        MatchViewSet.update = mock_update
        match_obj = Match.objects.get(id=objeto.id)
        print(match_obj)
        response = MatchViewSet.update(objeto,json_match)


        assert response.status_code == 400
        
    """
        COMPONENT / DB INTEGRATION TEST:
        Check update method in Match with date blank
    """
    @pytest.mark.django_db
    def test_update_match_date_blank(self):

        
        """
        Check update method in match.
        """

        objeto = Match.objects.create(
            user_id = 6,
            opponent = 'Sevilla',
            is_local = True,
            alignment ='4-3-3',
            url= 'https://www.google.com/webhp',
            city ='Barcelona',
            weather = 'clear',
            start_date = '2023-01-11T13:38:00Z',
            sent_email = False
        )

        json_match = {
            'id':objeto.id,
            'user_id' : 6,
            'opponent' : '',
            'is_local' : True,
            'alignment' : '4-2-1',
            'url': 'https://www.google.com/webhp',
            'city' :'Caracas',
            'weather' : 'clear',
            'start_date' : '',
            'sent_email' : False
            
        }

        
        MatchViewSet.update = mock_update
        match_obj = Match.objects.get(id=objeto.id)
        print(match_obj)
        response = MatchViewSet.update(objeto,json_match)


        assert response.status_code == 400


    """
        COMPONENT / DB INTEGRATION TEST:
        Check delete method in match.
    """
    @pytest.mark.django_db
    def test_delete_match(self):

        def mock_delete(id):
            
            match = Match.objects.filter(id=id)
            
            
            if(match):
                match.delete()
                return Response(status=204)
            else:
                return Response(status=404)
            
            
        

        objeto = Match.objects.create(
            user_id = 6,
            opponent = 'Sevilla',
            is_local = True,
            alignment ='4-3-3',
            url= 'https://www.google.com/webhp',
            city ='Barcelona',
            weather = 'clear',
            start_date = '2023-01-11T13:38:00Z',
            sent_email = False
        )
        
        MatchViewSet.delete = mock_delete
        
        response = MatchViewSet.delete(objeto.id)
        match_count = Match.objects.filter(id=objeto.id).count()
        

        assert response.status_code == 204
        assert match_count == 0


    """
        INTEGRATION TEST: 
        Check send email to team-service correctly
    """
    @pytest.mark.django_db
    def test_send_email(self):
        response = SendEmailSet.get(self, request='')
        assert response.status_code == 200
                  
            
    """
        INTEGRATION TEST: 
        Check openWeather is up
    """
    @pytest.mark.django_db
    def test_open_weather(self):
        city = 'Seville'
        open_weather_key = os.environ.get('OPEN_WEATHER_KEY', 'b8de83b3476d58590a4fbf3661f4dabe')
        response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key)
        assert response.status_code == 200

    """
        INTEGRATION TEST: 
        Check openWeather is up
    """
    @pytest.mark.django_db
    def test_open_weather_bad_token(self):
        city = 'Seville'
        open_weather_key = os.environ.get('OPEN_WEATHER_KEY', 'JAJANOENTRAS')
        response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key)
        assert response.status_code == 401

    """
        INTEGRATION TEST: 
        Check openWeather returns not valid city when random city is entered
    """
    @pytest.mark.django_db
    def test_open_weather_bad_city(self):
        city = 'Afgorjohnaf'
        open_weather_key = os.environ.get('OPEN_WEATHER_KEY', 'b8de83b3476d58590a4fbf3661f4dabe')
        response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + open_weather_key)
        assert response.status_code == 404
            
            
    """
        INTEGRATION TEST: 
        Check if fails sending email to team-service correctly
        when user_id is incorrect
    """
    @pytest.mark.django_db
    def test_send_email_bad_format(self):
        ls = {
                'alignment':"5-3-2",
                'city': "Seville",
                'id': "rwH9poGZngyHspOeOIEKQXeU",
                'is_local': 'True',
                'opponent': "Sevilla FC 2",
                'sent_email': 'False',
                'start_date': "2023-01-19T14:07:00Z",
                'url': "sevilla1",
                'user_id': '154787545',
                'weather': "scattered clouds - Temperatura: 17.19"
            }
        response = requests.post(team_url + 'send-email-player', data=ls)
        assert response.status_code == 500


    """
        INTEGRATION TEST: 
        Check send email to team-service correctly,
        another way to check
    """
    @pytest.mark.django_db
    def test_send_email_2(self):
        ls = {
                'alignment':"5-3-2",
                'city': "Seville",
                'id': "rwH9poGZngyHspOeOIEKQXeU",
                'is_local': True,
                'opponent': "Sevilla FC 2",
                'sent_email': False,
                'start_date': "2023-01-19T14:07:00Z",
                'url': "sevilla1",
                'user_id': 16,
                'weather': "scattered clouds - Temperatura: 17.19"
            }
        response = requests.post(team_url + 'send-email-player', data=ls)
        assert response.status_code == 200

    """
        INTEGRATION TEST: 
        Check if fails sending email to team-service correctly
        when user_id is incorrect
    """
    @pytest.mark.django_db
    def test_send_email_bad_user_id(self):
        ls = {
                'alignment':"5-3-2",
                'city': "Seville",
                'id': "rwH9poGZngyHspOeOIEKQXeU",
                'is_local': True,
                'opponent': "Sevilla FC 2",
                'sent_email': False,
                'start_date': "2023-01-19T14:07:00Z",
                'url': "sevilla1",
                'user_id': 154787545,
                'weather': "scattered clouds - Temperatura: 17.19"
            }
        response = requests.post(team_url + 'send-email-player', data=ls)
        assert response.status_code == 500
    """
        INTEGRATION MONGODB TEST: 
        Check if connects to DB
    """
    @pytest.mark.django_db
    def test_mongo_db_conn(self):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            assert False
        else:
            assert True
