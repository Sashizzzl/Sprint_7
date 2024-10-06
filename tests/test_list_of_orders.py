import requests
from config import URL
from helpers import OrderData
import allure

class TestListOfOrders:
    @allure.title('Проверка возврата списка заказов в тело ответа запроса на получение списка заказов')
    def test_get_orders_response_text_contains_list_if_orders(self):
        response = requests.get(f'{URL}/api/v1/orders')
        assert 'orders' in response.text
        assert response.status_code == 200
