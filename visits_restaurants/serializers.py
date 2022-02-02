from typing import Dict
from django.db.models import Avg, Sum
from rest_framework import serializers
from visits_restaurants.models import Restaurant, Visit


class RestaurantSerializer(serializers.ModelSerializer):
    """Restaurant serializer excluding a creator from writing
    """
    class Meta:
        model = Restaurant
        fields = "__all__"
        extra_kwargs = {"creator": {"read_only": True}}


class VisitSerializer(serializers.ModelSerializer):
    """Visit serializer excluding a date of creation from writing
    """
    class Meta:
        model = Visit
        fields = "__all__"
        extra_kwargs = {"date": {"read_only": True}}


class VisitsDateSerializer(serializers.Serializer):
    """Auxiliary serializer if visits generates only dates in a list
    """
    def to_representation(self, instance):
        return instance.date

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class RestaurantAggregatedSerializer(serializers.ModelSerializer):
    """Serializer aggregating visits for summary view
    """
    aggregates = serializers.SerializerMethodField()
    visits = VisitsDateSerializer(many=True)

    class Meta:
        model = Restaurant
        exclude = ["creator"]

    def get_aggregates(self, obj: Restaurant) -> Dict[str, float]:
        return obj.visits.aggregate(rating=Avg("evaluation"), spending=Sum("expense"))
