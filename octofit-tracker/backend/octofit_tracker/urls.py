"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from octofit_tracker.views import (
    OCUserViewSet,
    TeamViewSet,
    ActivityViewSet,
    LeaderboardViewSet,
    WorkoutViewSet,
    health_check,
)

router = DefaultRouter()
router.register(r'users', OCUserViewSet, basename='ocuser')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')


@api_view(['GET'])
def api_root(request):
    """API Root endpoint"""
    return Response({
        'message': 'OctoFit Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'users': request.build_absolute_uri('/users/'),
            'teams': request.build_absolute_uri('/teams/'),
            'activities': request.build_absolute_uri('/activities/'),
            'leaderboard': request.build_absolute_uri('/leaderboard/'),
            'workouts': request.build_absolute_uri('/workouts/'),
            'health': request.build_absolute_uri('/health/'),
        }
    })


urlpatterns = [
    path('', api_root, name='api_root'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
]
