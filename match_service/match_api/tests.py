from django.test import TestCase

import pytest
from .models import Match
from .serializers import MatchSerializer
# Create your tests here.




@pytest.mark.django_db
def test_create_match(client):

    request_url = '/api/v1/match/'

    """
    Check create method in Match.
    """
    json_match = {
                "id": "",
                "local": "",
                "visitor": "",
                "alignment": "",
                "url": "",
                "weather": "",
                "start_date": "",
                "created_by_local": True,
                "accepted": True,
            }

    response = client.post(request_url, data=json_match, format='json')

    match = MatchSerializer(data=json_match)
    match.is_valid()

    assert response.status_code == 201

    # Delete created_at and updated_at fields
    response_dic = dict(response.data)
    response_dic.pop('created_at')
    response_dic.pop('updated_at')

    assert response_dic == match.data


@pytest.mark.django_db
def test_update_match(client):

    request_url = '/api/v1/match/<pk>'
    
    """
    Check update method in match.
    """
    json_match = {
        "url": "",
        "alignment": ""
        
    }

    url = request_url + '<pk>'
    response = client.put(url, data=json_match, content_type='application/json')

    match = MatchSerializer(data=json_match)
    match.is_valid()

    assert response.status_code == 200

    response_dic = dict(response.data)
    response_dic.pop('created_at')
    response_dic.pop('updated_at')

    assert response.status_code == 200
    assert response_dic == match.data



