from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=200, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_starred = models.BooleanField(default=False)
    message_count = models.IntegerField(default=0)
    language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('kn', 'Kannada'),
    ])

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.farmer.username} - {self.title}"

    def get_context_messages(self, limit=10):
        """Get last N messages for AI context"""
        return list(self.messages.order_by('-timestamp')[:limit])[::-1]


class ChatMessage(models.Model):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant"), ("system", "System")]
    CATEGORY_CHOICES = [
        ('crop', 'Crop Advisory'),
        ('disease', 'Disease & Pest'),
        ('weather', 'Weather'),
        ('soil', 'Soil Management'),
        ('irrigation', 'Irrigation'),
        ('fertilizer', 'Fertilizer'),
        ('scheme', 'Govt Schemes'),
        ('market', 'Market & Mandi'),
        ('organic', 'Organic Farming'),
        ('general', 'General'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    confidence = models.FloatField(default=0.95)
    is_voice = models.BooleanField(default=False)
    has_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to='chat_images/%Y/%m/', null=True, blank=True)
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    language = models.CharField(max_length=5, default='en')

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class QuickQuestion(models.Model):
    """Pre-defined farming questions"""
    CATEGORY_CHOICES = ChatMessage.CATEGORY_CHOICES

    question = models.CharField(max_length=300)
    question_hi = models.CharField(max_length=300, blank=True, verbose_name='Hindi')
    question_kn = models.CharField(max_length=300, blank=True, verbose_name='Kannada')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=10, default='🌾')
    click_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-click_count']

    def __str__(self):
        return self.question


class FarmingTip(models.Model):
    """Daily rotating farming tips"""
    SEASON_CHOICES = [
        ('kharif', 'Kharif'),
        ('rabi', 'Rabi'),
        ('zaid', 'Zaid'),
        ('all', 'All Seasons'),
    ]

    tip = models.TextField()
    tip_hi = models.TextField(blank=True)
    tip_kn = models.TextField(blank=True)
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, default='all')
    category = models.CharField(max_length=20, default='general')
    icon = models.CharField(max_length=10, default='💡')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tip[:80]


class UserFeedback(models.Model):
    """Feedback on AI responses"""
    message = models.OneToOneField(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    rating = models.IntegerField(default=0)  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} for msg {self.message.id}"


class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chatbot_preferences",
    )
    theme = models.CharField(max_length=10, default='light', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
    ])
    language = models.CharField(max_length=10, default='en')
    voice_enabled = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    auto_translate = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.user.username}"
