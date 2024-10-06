import requests
from config import URL
from helpers import random_data
import allure
class TestCourierLogIn:
    @allure.title('Проверка возможности авторизации курьера')
    def test_courier_log_in_courier_sucessfuly_logged_in(self, register_new_courier_and_return_login_password, delete_courier):
        payload = {"login": register_new_courier_and_return_login_password[0],
                   "password": register_new_courier_and_return_login_password[1]}
        response = requests.post(f'{URL}/api/v1/courier/login', data=payload)
        assert response.status_code == 200
    @allure.title('Проверка возврата id курьера при успешном запросе на авторизацию')
    def test_text_of_courier_log_in_contains_id(self,register_new_courier_and_return_login_password, delete_courier):
        payload = {"login": register_new_courier_and_return_login_password[0],
                   "password": register_new_courier_and_return_login_password[1]}
        response = requests.post(f'{URL}/api/v1/courier/login', data=payload)
        assert 'id' in response.text
    @allure.title('Проверка необходимости передачи всх обязательных полей при авторизации курьера (возврат ошибки при отсутствии одного из полей)')
    def test_courier_log_in_demands_all_required_fields(self,register_new_courier_and_return_login_password, delete_courier):
        payload_1 = {"login": '',
                   "password": register_new_courier_and_return_login_password[1]}
        response_1 = requests.post(f'{URL}/api/v1/courier/login', data=payload_1)
        assert response_1.status_code == 400
        assert response_1.text == '{"code":400,"message":"Недостаточно данных для входа"}'
        payload_2 = {"login": register_new_courier_and_return_login_password[0],
                     "password":''}
        response_2 = requests.post(f'{URL}/api/v1/courier/login', data=payload_2)
        assert response_2.status_code == 400
        assert response_2.text == '{"code":400,"message":"Недостаточно данных для входа"}'
    @allure.title('Проверка возврата ошибки при указании неправильных логина или пароля')
    def test_error_when_login_or_password_incorrect(self,register_new_courier_and_return_login_password, delete_courier):
        payload_1 = {"login": f'register_new_courier_and_return_login_password[0]{random_data}',
                     "password": register_new_courier_and_return_login_password[1]}
        response_1 = requests.post(f'{URL}/api/v1/courier/login', data=payload_1)
        assert response_1.status_code == 404
        assert response_1.text == '{"code":404,"message":"Учетная запись не найдена"}'
        payload_2 = {"login": register_new_courier_and_return_login_password[0],
                     "password": f'register_new_courier_and_return_login_password[1]{random_data}'}
        response_2 = requests.post(f'{URL}/api/v1/courier/login', data=payload_2)
        assert response_2.status_code == 404
        assert response_2.text == '{"code":404,"message":"Учетная запись не найдена"}'
    @allure.title('Проверка возврата ошибки при авторизации под несуществующим пользователем')
    def test_error_log_in_with_non_existing_user_data(self):
        payload = {"login": random_data,
                     "password": random_data}
        response = requests.post(f'{URL}/api/v1/courier/login', data=payload)
        assert response.status_code == 404
        assert response.text == '{"code":404,"message":"Учетная запись не найдена"}'

