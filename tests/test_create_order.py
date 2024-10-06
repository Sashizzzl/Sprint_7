import requests
from config import URL
from helpers import OrderData
import pytest
import allure
class TestCreateOrder:
    @allure.title('Проверка содержания в теле ответа запроса на создание заказа элемента "track"')
    def test_create_order_response_text_contains_track(self):
        payload = OrderData.order_black
        response = requests.post(f'{URL}/api/v1/orders',json=payload)
        assert response.status_code == 201
        assert 'track' in response.text
    @allure.title('Проверка возможности не указывать цвет при создании заказа')
    def test_create_order_without_colour_order_created(self):
        payload = OrderData.order_no_colour
        response = requests.post(f'{URL}/api/v1/orders', json=payload)
        assert response.status_code == 201
        assert 'track' in response.text
    @allure.title('Проверка возможности указания обоих цветов при создании заказа')
    def test_create_order_choose_both_colours_order_created(self):
        payload = OrderData.order_both_colours
        response = requests.post(f'{URL}/api/v1/orders', json=payload)
        assert response.status_code == 201
        assert 'track' in response.text
    @allure.title('Проверка возможности указания одного из цветов — BLACK или GREY при создании заказа')
    @pytest.mark.parametrize("payload", [OrderData.order_black,OrderData.order_grey])
    def test_create_order_choose_black_or_grey_colour_order_created(self,payload):
        response = requests.post(f'{URL}/api/v1/orders', json=payload)
        assert response.status_code == 201
        assert 'track' in response.text