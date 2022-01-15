import json
from django.test import TestCase

# Create your tests here.


def set_token_bearer(self):
    res = self.client.post("/api/token/",
                           data={"email": "michal.mladek@nic.cz", "password": "kalamita123"},
                           content_type="application/json"
                           )
    token = json.loads(res.content)["access"]
    self.bearer_token = f"Bearer {token}"


class CreateVisitTestCase(TestCase):
    fixtures = ["user.json", "restaurant.json", "visit.json"]

    def setUp(self) -> None:
        set_token_bearer(self)

    def test_creator_can_create_visit(self):
        res = self.client.post("/api/visits/",
                               data={
                                   "expense": 135.5,
                                   "note": "It was somehow very weird!",
                                   "evaluation": 2,
                                   "restaurant": 1
                               },
                               HTTP_AUTHORIZATION=self.bearer_token
                               )
        self.assertEqual(res.status_code, 201)

    def test_creator_cannot_create_visit(self):
        res = self.client.post("/api/visits/",
                               data={
                                   "expense": 135.5,
                                   "note": "It was somehow very weird!",
                                   "evaluation": 2,
                                   "restaurant": 4
                               },
                               HTTP_AUTHORIZATION=self.bearer_token
                               )
        self.assertEqual(res.status_code, 403)


class AggregatedRestaurantsTestCase(TestCase):
    fixtures = ["user.json", "restaurant.json", "visit.json"]

    def setUp(self) -> None:
        set_token_bearer(self)

    def test_restaurant_aggreated(self):
        res = self.client.get("/api/aggregated/1/", HTTP_AUTHORIZATION=self.bearer_token)
        expected_res = {
            "id": 1,
            "aggregates": {
                "rating": 3.6666666666666665,
                "spending": 681.5
            },
            "visits": [
                "2022-01-16",
                "2022-01-16",
                "2022-01-16"
            ],
            "name": "Spojovna",
            "place": "Praha 11",
            "type": "CZ"
        }
        self.assertEqual(json.loads(res.content), expected_res)
