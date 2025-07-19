from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

User = get_user_model()

class UsernameCheckView(APIView):
    def get(self, request):
        username = request.query_params.get('username', '').strip()

        # Basic validation rules (you can customize)
        if not username.isalnum() or len(username) < 3:
            return Response(
                {"valid": False, "error": "Username must be at least 3 characters and alphanumeric."},
            )

        # Check availability
        if User.objects.filter(username=username).exists():
            return Response({"valid": False, "error": "Username is already taken."})
        
        return Response({"valid": True})


class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({"users": []})  # return empty if no query

        # Search for usernames starting with the query (case-insensitive)
        users = User.objects.filter(username__istartswith=query)[:10]

        return Response({
            "users": [user.username for user in users]
        }, status=status.HTTP_200_OK)
