from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from visits_restaurants.models import Restaurant
from visits_restaurants.serializers import RestaurantSerializer, RestaurantAggregatedSerializer


class CreateRestaurantMixin(mixins.CreateModelMixin):
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UpdateRestaurantMixin(mixins.UpdateModelMixin):
    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)


class RestaurantViewset(  # pylint: disable=too-many-ancestors
    CreateRestaurantMixin, UpdateRestaurantMixin,
        viewsets.ModelViewSet):
    """This viewset opens endpoints for restaurant creation and updating
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["pk", "name"]
    ordering = ["pk"]


class RestaurantAggregatedViewset(  # pylint: disable=too-many-ancestors
        viewsets.ReadOnlyModelViewSet):
    """This viewset opens summary endpoints for listing and detail view
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantAggregatedSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "place"]
    ordering_fields = ["name", "place", "type"]
    ordering = ["name"]
