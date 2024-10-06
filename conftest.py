import pytest
import requests
import random
import string
from config import URL

@pytest.fixture
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(f'{URL}/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass

@pytest.fixture
def delete_courier(register_new_courier_and_return_login_password):
    payload = {"login": register_new_courier_and_return_login_password[0],
              "password": register_new_courier_and_return_login_password[1],
               "firstName": register_new_courier_and_return_login_password[2]}
    yield
    #получаем ID курьера
    response_1 = requests.post(f'{URL}/api/v1/courier/login', data = payload)
    id = response_1.json()['id']
    # удаляем созданного курьера
    response_2 = requests.delete(f'{URL}/api/v1/courier/{id}')
    assert response_2.status_code == 200
    assert response_2.text == '{"ok":true}'
