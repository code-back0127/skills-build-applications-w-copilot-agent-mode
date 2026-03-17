from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import OCUser, Team, Activity, Leaderboard, Workout
from datetime import datetime, date


class OCUserModelTest(TestCase):
    """OCUser 모델 테스트"""
    
    def setUp(self):
        self.user = OCUser.objects.create(
            email='test@example.com',
            username='testuser',
            full_name='Test User'
        )
    
    def test_create_user(self):
        """사용자 생성 테스트"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.full_name, 'Test User')
    
    def test_user_unique_email(self):
        """이메일 고유성 테스트"""
        with self.assertRaises(Exception):
            OCUser.objects.create(
                email='test@example.com',
                username='anotheruser',
                full_name='Another User'
            )


class TeamModelTest(TestCase):
    """Team 모델 테스트"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_create_team(self):
        """팀 생성 테스트"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Activity 모델 테스트"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@example.com',
            activity_type='Running',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            activity_date=date.today()
        )
    
    def test_create_activity(self):
        """활동 생성 테스트"""
        self.assertEqual(self.activity.user_email, 'test@example.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.calories_burned, 300)


class LeaderboardModelTest(TestCase):
    """Leaderboard 모델 테스트"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_email='test@example.com',
            team_name='Test Team',
            total_calories=3000,
            total_activities=10,
            rank=1
        )
    
    def test_create_leaderboard(self):
        """리더보드 항목 생성 테스트"""
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertEqual(self.leaderboard.total_calories, 3000)
        self.assertEqual(self.leaderboard.total_activities, 10)


class WorkoutModelTest(TestCase):
    """Workout 모델 테스트"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            user_email='test@example.com',
            workout_name='Full Body',
            exercises=['Squats', 'Bench Press'],
            duration_minutes=60,
            difficulty='Hard'
        )
    
    def test_create_workout(self):
        """운동 계획 생성 테스트"""
        self.assertEqual(self.workout.workout_name, 'Full Body')
        self.assertEqual(self.workout.difficulty, 'Hard')
        self.assertEqual(len(self.workout.exercises), 2)


class OCUserAPITest(APITestCase):
    """OCUser API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = OCUser.objects.create(
            email='api@example.com',
            username='apiuser',
            full_name='API User'
        )
    
    def test_get_users(self):
        """사용자 목록 조회 테스트"""
        response = self.client.get(reverse('ocuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
    
    def test_create_user(self):
        """사용자 생성 API 테스트"""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'full_name': 'New User'
        }
        response = self.client.post(reverse('ocuser-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OCUser.objects.count(), 2)
    
    def test_update_user(self):
        """사용자 업데이트 테스트"""
        data = {
            'email': 'api@example.com',
            'username': 'updated_user',
            'full_name': 'Updated User'
        }
        response = self.client.put(
            reverse('ocuser-detail', kwargs={'pk': self.user.id}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_user')


class TeamAPITest(APITestCase):
    """Team API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='API Team',
            description='Test team for API'
        )
    
    def test_get_teams(self):
        """팀 목록 조회 테스트"""
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
    
    def test_create_team(self):
        """팀 생성 API 테스트"""
        data = {
            'name': 'New Team',
            'description': 'A new team'
        }
        response = self.client.post(reverse('team-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class ActivityAPITest(APITestCase):
    """Activity API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity = Activity.objects.create(
            user_email='test@example.com',
            activity_type='Running',
            duration_minutes=30,
            calories_burned=300,
            activity_date=date.today()
        )
    
    def test_get_activities(self):
        """활동 목록 조회 테스트"""
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)


class LeaderboardAPITest(APITestCase):
    """Leaderboard API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard = Leaderboard.objects.create(
            user_email='test@example.com',
            team_name='Test Team',
            total_calories=3000,
            total_activities=10,
            rank=1
        )
    
    def test_get_leaderboard(self):
        """리더보드 조회 테스트"""
        response = self.client.get(reverse('leaderboard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)


class WorkoutAPITest(APITestCase):
    """Workout API 테스트"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            user_email='test@example.com',
            workout_name='Full Body',
            exercises=['Squats', 'Bench Press'],
            duration_minutes=60,
            difficulty='Hard'
        )
    
    def test_get_workouts(self):
        """운동 계획 목록 조회 테스트"""
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
