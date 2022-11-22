from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView
    )
from .serializers import MatchSerializer
from .models import Match
# Create your views here.


class MatchListApiView(ListAPIView):

    serializer_class = MatchSerializer

    def get_queryset(self):
        return Match.objects.all()

class MatchCreateApiView(CreateAPIView):
    serializer_class = MatchSerializer

class MacthRetrieveApiView(RetrieveAPIView):
    serializer_class = MatchSerializer
    queryset = Match.objects.filter()

class MatchDestroyApiView(DestroyAPIView):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

class MatchUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()