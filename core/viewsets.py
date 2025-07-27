from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

class WithUserAsCreator(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Customize the create process here
        message = serializer.save(creator = request.user)
        serializer = self.serializer_class(message)

        return Response(serializer.data)