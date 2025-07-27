from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]