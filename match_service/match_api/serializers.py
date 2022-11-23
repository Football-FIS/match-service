from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Match
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }