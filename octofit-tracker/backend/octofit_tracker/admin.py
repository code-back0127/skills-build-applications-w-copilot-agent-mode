from django.contrib import admin
from .models import OCUser, Team, Activity, Leaderboard, Workout


@admin.register(OCUser)
class OCUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'full_name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('email', 'username', 'full_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('기본 정보', {
            'fields': ('email', 'username', 'full_name')
        }),
        ('프로필', {
            'fields': ('profile_picture',)
        }),
        ('시간정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('팀 정보', {
            'fields': ('name', 'description', 'icon')
        }),
        ('시간정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'activity_type', 'duration_minutes', 'calories_burned', 'activity_date')
    list_filter = ('activity_type', 'activity_date', 'created_at')
    search_fields = ('user_email', 'activity_type', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('활동 정보', {
            'fields': ('user_email', 'activity_type', 'activity_date')
        }),
        ('활동 데이터', {
            'fields': ('duration_minutes', 'calories_burned', 'distance_km')
        }),
        ('추가 정보', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('시간정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_email', 'team_name', 'total_calories', 'total_activities')
    list_filter = ('team_name', 'rank', 'updated_at')
    search_fields = ('user_email', 'team_name')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('순위 정보', {
            'fields': ('rank', 'user_email', 'team_name')
        }),
        ('통계', {
            'fields': ('total_calories', 'total_activities')
        }),
        ('시간정보', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('workout_name', 'user_email', 'difficulty', 'duration_minutes', 'created_at')
    list_filter = ('difficulty', 'created_at', 'updated_at')
    search_fields = ('workout_name', 'user_email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('운동 정보', {
            'fields': ('user_email', 'workout_name', 'difficulty')
        }),
        ('운동 데이터', {
            'fields': ('exercises', 'duration_minutes')
        }),
        ('시간정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
