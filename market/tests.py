from rest_framework.test import APIClient, APITestCase


class MarketTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.client.post(
            "/api/user/registration/",
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        response = self.client.post(
            "/api/user/login/", {"username": "testuser", "password": "testpassword"}
        )
        token = response.json()["key"]
        self.client.headers = {"Authorization": f"Token {token}"}
        return super().setUp()

    def test_create_market(self):
        resp = self.client.post(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        market = resp.json()
        assert 'id' in market.keys()

    def test_create_store(self):
        resp = self.client.post(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        resp = self.client.get(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        market_id = resp.json()[-1]["id"]
        resp = self.client.post(
            "/api/market/stores/",
            data={"name": "xz collections", "market": market_id},
            headers=self.client.headers,
        )
        assert 'id' in resp.json().keys()

    def test_create_product(self):
        resp = self.client.post(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        resp = self.client.get(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        markets = resp.json()
        resp = self.client.post(
            "/api/market/stores/",
            data={"name": "xz collections", "market": markets[-1]['id']},
            headers=self.client.headers,
        )
        resp = self.client.get(
            "/api/market/stores/",
            headers=self.client.headers,
        )
        stores = resp.json()

        resp = self.client.post(
            "/api/market/products/",
            data={"name": "sport-shoes", "store": stores[-1]['id'],'price':100},
            headers=self.client.headers,
        )
        
        resp = self.client.get(
            "/api/market/products/",
        )
        products = resp.json()
        assert 'id' in products[-1].keys()
        