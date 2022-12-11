from django.test import TestCase

import pytest
from .models import Match
from .serializers import MatchSerializer
# Create your tests here.


@pytest.mark.django_db
def test_list_match(client):

    request_url = '/api/v1/match/list'

    """
    Check list method in match.
    """
    response = client.get(request_url)

    match = Match.objects.all()
    expected_data = list(match.values_list("id", flat=True))
                    

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_create_match(client):

    request_url = '/api/v1/match/'

    """
    Check create method in Match.
    """
    json_match = {
                "id": "4",
                "local": "sevilla",
                "visitor": "barcelona",
                "alignment": "4-3-3",
                "url": "https://www.google.com/?hl=es",
                "weather": "soleado",
                "start_date": "2022-12-11T09:24:00Z",
                "created_by_local": True,
                "accepted": True,
            }

    response = client.post(request_url, data=json_match, format='json')

    match = MatchSerializer(data=json_match)
    match.is_valid()

    assert response.status_code == 201


'''@pytest.mark.django_db
def test_update_match(client):

    request_url = '/api/v1/match/'
    
    """
    Check update method in match.
    """
    json_match = {
        "id": 2,
        "year_in_school": "SO",
        "local": "real madrid",
        "visitor": "barcelona",
        "alignment": "4-5-5",
        "url": "https://es.wikipedia.org/wiki/Wikipedia:Portada",
        "weather": "lluvioso",
        "start_date": "2022-09-29T09:24:00Z",
        "created_by_local": True,
        "accepted": True
        
    }

    url = request_url + '2'
    response = client.put(url, data=json_match, content_type='application/json')

    match = MatchSerializer(data=json_match)
    match.is_valid()

    assert response.status_code == 200'''


#da un error 404
@pytest.mark.django_db
def test_delete_match(client):

    request_url = '/api/v1/match/'

    """
    Check delete method in match.
    """
    #este id es de mi base local, se debe cambiar por la adeacuada
    url = request_url + 'QXLvszxykRklgexpag2YUzg0'
    response = client.delete(url, content_type='application/json')

    match_count = Match.objects.filter(id='QXLvszxykRklgexpag2YUzg0').count()

    assert response.status_code == 204
    assert match_count == 0


