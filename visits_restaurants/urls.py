from django.urls import path
from rest_framework.routers import DefaultRouter
from visits_restaurants.viewsets import RestaurantViewset, RestaurantAggregatedViewset
from visits_restaurants.views import CreateVisitView


restaurants_router = DefaultRouter()
restaurants_router.register(r"restaurants", RestaurantViewset)
restaurants_router.register(r"aggregated", RestaurantAggregatedViewset, basename="aggregated")

urlpatterns = [
    path("visits/", CreateVisitView.as_view())
] + restaurants_router.urls
