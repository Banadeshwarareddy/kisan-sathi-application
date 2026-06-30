from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Main chat page
    path('', 
         views.ChatPageView.as_view(), 
         name='home'),
    
    # Message
    path('api/message/', 
         views.SendMessageView.as_view(), 
         name='send-message'),
    
    # Sessions
    path('api/sessions/', 
         views.SessionListView.as_view(), 
         name='sessions'),
    
    path('api/sessions/<uuid:session_id>/', 
         views.SessionDetailView.as_view(), 
         name='session-detail'),
    
    # Quick questions & tips
    path('api/quick-questions/', 
         views.QuickQuestionsView.as_view(), 
         name='quick-questions'),
    
    path('api/daily-tip/', 
         views.DailyTipView.as_view(), 
         name='daily-tip'),
    
    # Feedback
    path('api/feedback/<uuid:message_id>/', 
         views.MessageFeedbackView.as_view(), 
         name='feedback'),
    
    # Utilities
    path('api/status/', 
         views.AIStatusView.as_view(), 
         name='ai-status'),
    
    path('api/stats/', 
         views.ChatStatsView.as_view(), 
         name='stats'),
    
    path('api/search/', 
         views.SearchMessagesView.as_view(), 
         name='search'),
]
