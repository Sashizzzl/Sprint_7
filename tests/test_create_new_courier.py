import requests
from config import URL
from helpers import random_data
import pytest
import allure
class TestCreateNewCourier:
    @allure.title('Проверка создания курьера(возврат правильного кода ответа и текста {"ok":true}')
    def test_create_new_courier_courier_is_created(self):
        #созаем курьера
        payload = {"login":random_data,
                   "password":random_data,
                   "firstName":random_data}
        response = requests.post(f'{URL}/api/v1/courier', data = payload)
        assert response.status_code == 201
        assert response.text == '{"ok":true}'
        # логинимся с созданными данными, чтобы получить ID курьера для его последующего удаления
        response_1 = requests.post(f'{URL}/api/v1/courier/login', data = payload)
        assert response_1.status_code == 200
        id = response_1.json()['id']
        #удаляем созданного курьера
        response_2 = requests.delete(f'{URL}/api/v1/courier/{id}')
        assert response_2.status_code == 200
        assert response_2.text == '{"ok":true}'
    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_impossible_to_create_two_couriers_with_same_data(self,register_new_courier_and_return_login_password, delete_courier):
        payload = {"login":register_new_courier_and_return_login_password[0],
                   "password":register_new_courier_and_return_login_password[1],
                   "firstName":register_new_courier_and_return_login_password[2]}
        response = requests.post(f'{URL}/api/v1/courier', data = payload)
        assert response.status_code == 409
        assert response.text == '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}'
    @allure.title('Проверка необходимости передачи всех обязательных полей в ручку при создании курьера (возвращается ошибка, если нет одного из полей)')
    @pytest.mark.parametrize("payload",[{"login":'',
            "password":random_data,
            "firstName":random_data}, {"login": random_data,
            "password": '',
            "firstName":random_data}])
    def test_create_courier_without_login_or_password_courier_impossible_to_create(self, payload):
        response_1 = requests.post(f'{URL}/api/v1/courier', data = payload)
        assert response_1.status_code == 400
        assert response_1.text == '{"code":400,"message":"Недостаточно данных для создания учетной записи"}'
    @allure.title('Проверка возвращения ошибки при создании курьера с уже существующим логином')
    def test_create_two_couriers_with_same_login_second_courier_impossible_to_create(self,register_new_courier_and_return_login_password,delete_courier):
        courier_login = register_new_courier_and_return_login_password[0]  # создаем курьера
        payload = {"login":courier_login,
                   "password":random_data,
                   "firstName":random_data}
        response = requests.post(f'{URL}/api/v1/courier', data=payload)
        assert response.status_code == 409
        assert response.text == '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}'
