from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import OCUser, Team, Activity, Leaderboard, Workout
from .serializers import (
    OCUserSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OCUserViewSet(viewsets.ModelViewSet):
    queryset = OCUser.objects.all()
    serializer_class = OCUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email', 'username']
    search_fields = ['email', 'username', 'full_name']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """이메일로 사용자 조회"""
        email = request.query_params.get('email')
        if email:
            user = self.queryset.filter(email=email).first()
            if user:
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'activity_type', 'activity_date']
    search_fields = ['user_email', 'activity_type', 'notes']
    ordering_fields = ['activity_date', 'calories_burned', 'created_at']
    ordering = ['-activity_date']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """사용자별 활동 조회"""
        user_email = request.query_params.get('email')
        if user_email:
            activities = self.queryset.filter(user_email=user_email)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """활동 요약 통계"""
        user_email = request.query_params.get('email')
        if user_email:
            activities = self.queryset.filter(user_email=user_email)
            total_activities = activities.count()
            total_calories = sum([a.calories_burned for a in activities])
            total_duration = sum([a.duration_minutes for a in activities])
            
            return Response({
                'user_email': user_email,
                'total_activities': total_activities,
                'total_calories': total_calories,
                'total_duration_minutes': total_duration,
                'average_calories': total_calories // total_activities if total_activities > 0 else 0,
                'average_duration': total_duration // total_activities if total_activities > 0 else 0,
            })
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team_name', 'rank']
    search_fields = ['user_email', 'team_name']
    ordering_fields = ['rank', 'total_calories', 'total_activities']
    ordering = ['rank']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """팀별 리더보드 조회"""
        team_name = request.query_params.get('team')
        if team_name:
            leaderboard = self.queryset.filter(team_name=team_name).order_by('rank')
            serializer = self.get_serializer(leaderboard, many=True)
            return Response(serializer.data)
        return Response({'error': 'Team parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'difficulty']
    search_fields = ['user_email', 'workout_name']
    ordering_fields = ['difficulty', 'duration_minutes', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """사용자별 운동 계획 조회"""
        user_email = request.query_params.get('email')
        if user_email:
            workouts = self.queryset.filter(user_email=user_email)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """난이도별 운동 계획 조회"""
        difficulty = request.query_params.get('level')
        if difficulty:
            workouts = self.queryset.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Level parameter required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'OK', 'message': 'OctoFit Tracker API is running'})
