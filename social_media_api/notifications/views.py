from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

# Create your views here.

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = request.user.notifications.all().order_by('-timestamp')
        unread_notifications = notifications.filter(read=False)

        response_data = {
            'unread_count': unread_notifications.count(),
            'notifications': [
                {
                    'id': n.id,
                    'actor': n.actor.username,
                    'verb': n.verb,
                    'target': str(n.target),
                    'timestamp': n.timestamp,
                    'read': n.read,
                }
                for n in notifications
            ]
        }
        return Response(response_data, status=200)