from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import (ChatSession, ChatMessage, QuickQuestion, FarmingTip)
from .ai_service import kisan_ai, detect_category
import json
import uuid
import random
from datetime import datetime, timedelta


# ── MAIN PAGE VIEW ───────────────────────────────────────────
class ChatPageView(LoginRequiredMixin, View):
    """Render full chat page"""
    login_url = '/accounts/login/'
    
    def get(self, request):
        # Get or create active session
        session = ChatSession.objects.filter(
            farmer=request.user, 
            is_active=True
        ).first()
        
        if not session:
            new_uuid = uuid.uuid4()
            session = ChatSession.objects.create(
                id=new_uuid,
                farmer=request.user,
                session_id=str(new_uuid),
                title='New Conversation'
            )
        
        # Get recent sessions for sidebar
        recent_sessions = ChatSession.objects.filter(
            farmer=request.user
        ).order_by('-updated_at')[:10]
        
        # Get quick questions
        quick_questions = QuickQuestion.objects.filter(
            is_active=True
        ).order_by('order')[:12]
        
        # Get daily farming tip
        all_tips = FarmingTip.objects.filter(is_active=True)
        tip = random.choice(all_tips) if all_tips.exists() else None
        
        # Get user stats
        total_msgs = ChatMessage.objects.filter(
            session__farmer=request.user,
            role='user'
        ).count()
        
        context = {
            'current_session': session,
            'recent_sessions': recent_sessions,
            'quick_questions': quick_questions,
            'daily_tip': tip,
            'total_messages': total_msgs,
            'ai_status': 'online' if kisan_ai.is_ready else 'fallback',
        }
        
        return render(request, 'chatbot/home.html', context)


# ── SEND MESSAGE API ────────────────────────────────────────
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id')
        language = request.data.get('language', 'en')
        is_voice = request.data.get('is_voice', False)
        
        # Validation
        if not message:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(message) > 2000:
            return Response(
                {'error': 'Message too long (max 2000 chars)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create session
        session = None
        if session_id:
            # First try to parse as UUID
            try:
                uuid_obj = uuid.UUID(session_id)
                # It's a valid UUID, try to find by id
                try:
                    session = ChatSession.objects.get(
                        id=uuid_obj,
                        farmer=request.user
                    )
                except ChatSession.DoesNotExist:
                    pass
            except (ValueError, AttributeError):
                # Not a valid UUID, try by session_id string
                try:
                    session = ChatSession.objects.get(
                        session_id=session_id,
                        farmer=request.user
                    )
                except ChatSession.DoesNotExist:
                    pass
        
        # Create new session if not found
        if not session:
            new_uuid = uuid.uuid4()
            session = ChatSession.objects.create(
                id=new_uuid,
                farmer=request.user,
                session_id=str(new_uuid),
                language=language
            )
        
        # Auto-update session title from first message
        if session.message_count == 0:
            title = message[:60] + ('...' if len(message) > 60 else '')
            session.title = title
        
        # Get conversation history for context
        history_msgs = session.get_context_messages(10)
        history = [{'role': m.role, 'content': m.content} 
                  for m in history_msgs]
        
        # Detect category
        category = detect_category(message)
        
        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=message,
            category=category,
            is_voice=is_voice,
            language=language,
        )
        
        # Get AI response
        result = kisan_ai.get_response(
            message=message,
            session_id=str(session.id),
            history=history,
            language=language
        )
        
        # Save AI response
        ai_msg = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=result['response'],
            category=result['category'],
            confidence=result['confidence'],
            tokens_used=result['tokens'],
            response_time=result['time'],
        )
        
        # Update session
        session.message_count += 2
        session.language = language
        session.save()
        
        # Generate follow-up suggestions
        suggestions = self.get_suggestions(result['category'], language)
        
        return Response({
            'success': True,
            'session_id': session.session_id,  # Return string session_id for JS
            'session_title': session.title,
            'message_id': str(ai_msg.id),
            'response': result['response'],
            'category': result['category'],
            'confidence': result['confidence'],
            'response_time': result['time'],
            'source': result['source'],
            'timestamp': ai_msg.timestamp.strftime('%I:%M %p'),
            'updated_at_iso': session.updated_at.isoformat(),
            'suggestions': suggestions,
        }, status=status.HTTP_200_OK)
    
    def get_suggestions(self, category: str, language: str) -> list:
        """Get follow-up question suggestions"""
        suggestions_map = {
            'crop': {
                'en': [
                    "Best fertilizer for this crop?",
                    "Common diseases of this crop?",
                    "When is the best time to harvest?"
                ],
                'hi': [
                    "इस फसल के लिए खाद क्या डालें?",
                    "इस फसल की बीमारियां क्या हैं?",
                    "कटाई का सही समय कब है?"
                ]
            },
            'disease': {
                'en': [
                    "Organic treatment options?",
                    "How to prevent this in future?",
                    "Which spray is most effective?"
                ],
                'hi': [
                    "जैविक उपाय क्या हैं?",
                    "भविष्य में कैसे बचें?",
                    "कौन सा स्प्रे सबसे अच्छा है?"
                ]
            },
            'scheme': {
                'en': [
                    "How to apply for PM-KISAN?",
                    "Documents needed for crop insurance?",
                    "What is Kisan Credit Card?"
                ],
                'hi': [
                    "पीएम-किसान के लिए कैसे आवेदन करें?",
                    "फसल बीमा के लिए कौन से दस्तावेज चाहिए?",
                    "किसान क्रेडिट कार्ड क्या है?"
                ]
            },
        }
        
        lang = language if language in ['en', 'hi'] else 'en'
        cat_suggestions = suggestions_map.get(category, {})
        return cat_suggestions.get(lang, cat_suggestions.get('en', []))


# ── SESSION MANAGEMENT APIs ─────────────────────────────────
class SessionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all chat sessions for sidebar"""
        sessions = ChatSession.objects.filter(
            farmer=request.user
        ).order_by('-updated_at')[:100]
        
        data = [{
            'id': str(s.id),
            'title': s.title,
            'message_count': s.message_count,
            'language': s.language,
            'is_starred': s.is_starred,
            'updated_at': s.updated_at.strftime('%d %b, %I:%M %p'),
            'updated_at_iso': s.updated_at.isoformat(),
            'created_at': s.created_at.strftime('%d %b %Y'),
        } for s in sessions]
        
        return Response({
            'sessions': data,
            'total': len(data)
        })
    
    def post(self, request):
        """Create new chat session"""
        new_uuid = uuid.uuid4()
        session = ChatSession.objects.create(
            id=new_uuid,
            farmer=request.user,
            session_id=str(new_uuid),
            title='New Conversation',
            language=request.data.get('language', 'en')
        )
        
        return Response({
            'session_id': str(session.id),
            'title': session.title,
        }, status=status.HTTP_201_CREATED)


class SessionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        """Get full message history for a session"""
        try:
            session = ChatSession.objects.get(
                id=session_id,
                farmer=request.user
            )
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        messages = session.messages.order_by('timestamp')
        
        data = [{
            'id': str(m.id),
            'role': m.role,
            'content': m.content,
            'category': m.category,
            'confidence': m.confidence,
            'is_voice': m.is_voice,
            'timestamp': m.timestamp.strftime('%I:%M %p'),
            'date': m.timestamp.strftime('%d %b %Y'),
            'is_liked': m.is_liked,
        } for m in messages]
        
        return Response({
            'session_id': str(session.id),
            'title': session.title,
            'language': session.language,
            'message_count': session.message_count,
            'messages': data,
            'created_at': session.created_at.strftime('%d %b %Y'),
        })
    
    def delete(self, request, session_id):
        """Delete a session"""
        try:
            session = ChatSession.objects.get(
                id=session_id, 
                farmer=request.user
            )
            session.delete()
            return Response({'message': 'Session deleted'})
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, session_id):
        """Star/rename a session"""
        try:
            session = ChatSession.objects.get(
                id=session_id, 
                farmer=request.user
            )
            
            if 'is_starred' in request.data:
                session.is_starred = request.data['is_starred']
            
            if 'title' in request.data:
                session.title = request.data['title'][:200]
            
            session.save()
            return Response({'message': 'Updated'})
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ── QUICK QUESTIONS & TIPS ──────────────────────────────────
class QuickQuestionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        questions = QuickQuestion.objects.filter(
            is_active=True
        ).order_by('order')[:16]
        
        lang = request.GET.get('lang', 'en')
        
        data = []
        for q in questions:
            text = q.question
            if lang == 'hi' and q.question_hi:
                text = q.question_hi
            elif lang == 'kn' and q.question_kn:
                text = q.question_kn
            
            data.append({
                'id': q.id,
                'question': text,
                'category': q.category,
                'icon': q.icon,
            })
        
        return Response({'questions': data})


class DailyTipView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lang = request.GET.get('lang', 'en')
        tips = FarmingTip.objects.filter(is_active=True)
        
        if not tips.exists():
            return Response({'tip': None})
        
        tip = random.choice(tips)
        text = tip.tip
        
        if lang == 'hi' and tip.tip_hi:
            text = tip.tip_hi
        elif lang == 'kn' and tip.tip_kn:
            text = tip.tip_kn
        
        return Response({
            'tip': text,
            'icon': tip.icon,
            'category': tip.category,
            'season': tip.season,
        })


# ── MESSAGE FEEDBACK ────────────────────────────────────────
class MessageFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, message_id):
        try:
            msg = ChatMessage.objects.get(
                id=message_id,
                session__farmer=request.user
            )
            
            action = request.data.get('action')
            
            if action == 'like':
                msg.is_liked = True
                msg.is_disliked = False
            elif action == 'dislike':
                msg.is_disliked = True
                msg.is_liked = False
            
            msg.save()
            return Response({'message': 'Feedback saved'})
        except ChatMessage.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ── AI STATUS ───────────────────────────────────────────────
class AIStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'status': 'online' if kisan_ai.is_ready else 'fallback',
            'model': kisan_ai.model if kisan_ai.is_ready else 'rule-based',
            'message': ('🟢 Kisan AI Online' 
                       if kisan_ai.is_ready 
                       else '🟡 Basic Mode'),
        })


# ── CHAT STATS ──────────────────────────────────────────────
class ChatStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        farmer = request.user
        
        total_sessions = ChatSession.objects.filter(
            farmer=farmer
        ).count()
        
        total_messages = ChatMessage.objects.filter(
            session__farmer=farmer, 
            role='user'
        ).count()
        
        # Category breakdown
        cat_data = ChatMessage.objects.filter(
            session__farmer=farmer,
            role='user'
        ).values('category').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return Response({
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'categories': list(cat_data),
        })


# ── SEARCH MESSAGES ─────────────────────────────────────────
class SearchMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if len(query) < 2:
            return Response({'results': []})
        
        messages = ChatMessage.objects.filter(
            session__farmer=request.user,
            content__icontains=query
        ).select_related('session').order_by('-timestamp')[:20]
        
        data = [{
            'message_id': str(m.id),
            'session_id': str(m.session.id),
            'session_title': m.session.title,
            'role': m.role,
            'content': m.content[:200],
            'timestamp': m.timestamp.strftime('%d %b, %I:%M %p'),
        } for m in messages]
        
        return Response({
            'results': data, 
            'count': len(data)
        })
