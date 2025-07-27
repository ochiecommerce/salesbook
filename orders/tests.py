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


    def test_create_order(self):
        resp = self.client.post(
            "/api/market/markets/", data={"name": "shoes"}, headers=self.client.headers
        )
        market = resp.json()
        assert 'id' in market.keys()
        resp = self.client.post(
            "/api/market/stores/",
            data={"name": "xz collections", "market": market['id']},
            headers=self.client.headers,
        )
        store = resp.json()
        assert 'id' in store.keys()
        resp = self.client.post(
            "/api/order/orders/", data={"items":[]}, headers=self.client.headers
        )
        order:dict = resp.json()
        assert 'id' in order.keys()
        resp = self.client.post(
            "/api/market/products/", data={'name':'sport-shoes','price':100,'store':store['id']}, headers=self.client.headers
        )
        product = resp.json()
        assert 'id' in product
        resp = self.client.post(
            "/api/order/orderitems/", data={"product":product['id'],'quantity':1,'order':order['id']}, headers=self.client.headers
        )
        order_item = resp.json()
        assert 'order' in order_item