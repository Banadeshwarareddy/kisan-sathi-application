from django.contrib import admin
from .models import (
    ChatSession, ChatMessage, QuickQuestion, 
    FarmingTip, UserFeedback, UserPreference
)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'title', 'message_count', 
                    'language', 'is_starred', 'created_at']
    list_filter = ['language', 'is_starred', 'is_active']
    search_fields = ['farmer__username', 'title', 'session_id']
    readonly_fields = ['session_id', 'message_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'category', 
                    'confidence', 'response_time', 'timestamp']
    list_filter = ['role', 'category', 'is_voice', 'language']
    search_fields = ['content', 'session__title']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(QuickQuestion)
class QuickQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'icon', 
                    'click_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'question_hi', 'question_kn']
    ordering = ['order', '-click_count']


@admin.register(FarmingTip)
class FarmingTipAdmin(admin.ModelAdmin):
    list_display = ['tip_preview', 'season', 'category', 
                    'icon', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['season', 'category', 'is_active']
    search_fields = ['tip', 'tip_hi', 'tip_kn']
    date_hierarchy = 'created_at'
    
    def tip_preview(self, obj):
        return obj.tip[:80] + '...' if len(obj.tip) > 80 else obj.tip
    tip_preview.short_description = 'Tip'


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'rating', 'created_at']
    list_filter = ['rating']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 
                    'voice_enabled', 'notifications_enabled']
    list_filter = ['theme', 'language', 'voice_enabled']
    search_fields = ['user__username']
