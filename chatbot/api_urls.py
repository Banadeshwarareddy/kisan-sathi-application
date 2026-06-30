from django.urls import path

from . import views


urlpatterns = [
    path("message/", views.ChatMessageView.as_view(), name="chatbot-message"),
    path("history/<str:session_id>/", views.ChatHistoryView.as_view(), name="chat-history"),
    path("session/new/", views.NewSessionView.as_view(), name="new-session"),
    path("status/", views.ChatbotStatusView.as_view(), name="chatbot-status"),
]
