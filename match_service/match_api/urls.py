from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('match/', views.MatchListApiView.as_view()),
    path('match/new', views.MatchCreateApiView.as_view()),
    path('match/detail/<pk>', views.MacthRetrieveApiView.as_view()),
    path('match/delete/<pk>', views.MatchDestroyApiView.as_view()),
    path('match/update/<pk>', views.MatchUpdateApiView.as_view()),
]