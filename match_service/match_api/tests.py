from django.test import TestCase
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from .models import Match
from .views import MatchViewSet
from .serializers import MatchSerializer
import pytest
# Create your tests here.


class TestCreate(TestCase):



    """
        Check create method in Match.
    """
    @pytest.mark.django_db
    def test_create_match(self):

        def mock_create(datos):
            serializador = MatchSerializer(data=datos)
            if serializador.is_valid():
                serializador.validated_data['weather'] = 'clear sky'
                #serializador.validated_data['weather'] = get_weather(datos['city'])
                serializador.save()
                return Response(serializador.data, status=201)
            else:
                return Response(serializador.data, status=400)

        
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
        Check update method in Match.
    """
    @pytest.mark.django_db
    def test_update_match(self):

        def mock_update(obj,datos):
            

            serializador = MatchSerializer(obj,data=datos,partial=True)
            print('------------serializador-------------')
            print(serializador)
            if serializador.is_valid():
                #serializador.validated_data['weather'] = 'clear sky'
                serializador.save()
                return Response(serializador.data, status=200)
            else:
                #print('------------serializador-------------')
                #print(serializador.errors)
                #print(serializador.data)
                return Response(serializador.data, status=400)
        
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
        #assert response.data.id == objeto.id


    """
        Check delete method in match.
    """
    @pytest.mark.django_db
    def test_delete_match(self):

        def mock_delete(id):
            
            match = Match.objects.filter(id=id)
            print(match)
            
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
        match_before = Match.objects.filter(id=objeto.id).count()
        print('-------------Before delete-------------')
        print(type(objeto.id))

        
        MatchViewSet.delete = mock_delete
        
        response = MatchViewSet.delete(objeto.id)
        match_count = Match.objects.filter(id=objeto.id).count()
        print('-------------After delete-------------')
        print(match_count)

        assert response.status_code == 204
        assert match_count == 0


