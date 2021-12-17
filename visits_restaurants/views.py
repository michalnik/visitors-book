from rest_framework import generics
from rest_framework import exceptions
from visits_restaurants.models import Visit, Restaurant
from visits_restaurants.serializers import VisitSerializer


class CreateVisitView(generics.CreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def perform_create(self, serializer):
        current_restaurant = Restaurant.objects.filter(
            pk=serializer.validated_data["restaurant"].pk,
            creator=self.request.user
        )
        if not current_restaurant:
            raise exceptions.PermissionDenied()
        serializer.save()
