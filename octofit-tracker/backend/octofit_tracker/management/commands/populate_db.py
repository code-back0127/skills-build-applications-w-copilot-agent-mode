from django.core.management.base import BaseCommand
from octofit_tracker.models import OCUser, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'octofit_db 데이터베이스에 테스트 데이터를 입력합니다.'

    def handle(self, *args, **options):
        # Clear existing data
        OCUser.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('기존 데이터 삭제 완료'))

        # Create Teams
        marvel_team = Team.objects.create(
            name='Marvel Team',
            description='Marvel Superheroes',
            icon='https://example.com/marvel.png'
        )
        dc_team = Team.objects.create(
            name='DC Team',
            description='DC Superheroes',
            icon='https://example.com/dc.png'
        )

        self.stdout.write(self.style.SUCCESS('팀 생성 완료'))

        # Create Users (Superheroes)
        marvel_users = [
            {'email': 'tony.stark@marvel.com', 'username': 'Iron Man', 'full_name': 'Tony Stark'},
            {'email': 'steve.rogers@marvel.com', 'username': 'Captain America', 'full_name': 'Steve Rogers'},
            {'email': 'natasha.romanoff@marvel.com', 'username': 'Black Widow', 'full_name': 'Natasha Romanoff'},
            {'email': 'bruce.banner@marvel.com', 'username': 'Hulk', 'full_name': 'Bruce Banner'},
        ]

        dc_users = [
            {'email': 'clark.kent@dc.com', 'username': 'Superman', 'full_name': 'Clark Kent'},
            {'email': 'bruce.wayne@dc.com', 'username': 'Batman', 'full_name': 'Bruce Wayne'},
            {'email': 'diana.prince@dc.com', 'username': 'Wonder Woman', 'full_name': 'Diana Prince'},
            {'email': 'barry.allen@dc.com', 'username': 'The Flash', 'full_name': 'Barry Allen'},
        ]

        users = []
        for user_data in marvel_users:
            user = OCUser.objects.create(**user_data)
            users.append((user, marvel_team))

        for user_data in dc_users:
            user = OCUser.objects.create(**user_data)
            users.append((user, dc_team))

        self.stdout.write(self.style.SUCCESS('사용자 생성 완료'))

        # Create Activities
        for idx, (user, team) in enumerate(users):
            for i in range(5):
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=['running', 'cycling', 'swimming', 'gym'][i % 4],
                    duration_minutes=(i + 1) * 30,
                    calories_burned=(i + 1) * 200 + 100,
                    distance_km=float((i + 1) * 2),
                    activity_date=datetime.now().date() - timedelta(days=i),
                    notes=f'Activity {i+1} for {user.username}'
                )

        self.stdout.write(self.style.SUCCESS('활동 생성 완료'))

        # Create Leaderboard entries
        rank = 1
        for user, team in users:
            total_activities = Activity.objects.filter(user_email=user.email).count()
            total_calories = sum([a.calories_burned for a in Activity.objects.filter(user_email=user.email)])
            
            Leaderboard.objects.create(
                user_email=user.email,
                team_name=team.name,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=rank
            )
            rank += 1

        self.stdout.write(self.style.SUCCESS('리더보드 생성 완료'))

        # Create Workouts
        workout_templates = [
            {
                'workout_name': 'Full Body Workout',
                'exercises': ['Squats', 'Bench Press', 'Deadlift'],
                'duration_minutes': 60,
                'difficulty': 'Hard'
            },
            {
                'workout_name': 'Cardio Session',
                'exercises': ['Running', 'Jump Rope', 'Burpees'],
                'duration_minutes': 30,
                'difficulty': 'Medium'
            },
            {
                'workout_name': 'Yoga Session',
                'exercises': ['Downward Dog', 'Warrior Pose', 'Child Pose'],
                'duration_minutes': 45,
                'difficulty': 'Easy'
            },
        ]

        for user, team in users:
            for template in workout_templates:
                Workout.objects.create(
                    user_email=user.email,
                    workout_name=template['workout_name'],
                    exercises=template['exercises'],
                    duration_minutes=template['duration_minutes'],
                    difficulty=template['difficulty']
                )

        self.stdout.write(self.style.SUCCESS('운동 계획 생성 완료'))
        self.stdout.write(self.style.SUCCESS('모든 테스트 데이터 입력 완료!'))
