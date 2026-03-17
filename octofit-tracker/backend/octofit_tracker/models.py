from django.db import models
from django.contrib.auth.models import User


class OCUser(models.Model):
    """User model for OctoFit Tracker"""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    profile_picture = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for OctoFit Tracker"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for OctoFit Tracker"""
    user_email = models.EmailField()
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    distance_km = models.FloatField(blank=True, null=True)
    activity_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user_email} - {self.activity_type}"


class Leaderboard(models.Model):
    """Leaderboard model for OctoFit Tracker"""
    user_email = models.EmailField()
    team_name = models.CharField(max_length=100)
    total_calories = models.IntegerField()
    total_activities = models.IntegerField()
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'

    def __str__(self):
        return f"{self.user_email} - Rank {self.rank}"


class Workout(models.Model):
    """Workout model for OctoFit Tracker"""
    user_email = models.EmailField()
    workout_name = models.CharField(max_length=200)
    exercises = models.JSONField()
    duration_minutes = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.workout_name
