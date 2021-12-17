from django.db.models import Avg, Sum
from rest_framework import serializers
from visits_restaurants.models import Restaurant, Visit


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        extra_kwargs = {"creator": {"read_only": True}}


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
        extra_kwargs = {"date": {"read_only": True}}


class VisitsDateSerializer(serializers.Serializer):
    def to_representation(self, data):
        return data.date

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class RestaurantAggregatedSerializer(serializers.ModelSerializer):
    aggregates = serializers.SerializerMethodField()
    visits = VisitsDateSerializer(many=True)

    class Meta:
        model = Restaurant
        exclude = ["creator"]

    def get_aggregates(self, obj):
        return obj.visits.aggregate(rating=Avg("evaluation"), spending=Sum("expense"))
