import time
import datetime as dt
from typing import Any, List
import requests
import config


def get(url: str, params: dict = {}, timeout: int = 5, max_retries: int = 555,
        backoff_factor: float = 0.3) -> requests.models.Response:
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response
        except:
            if i == max_retries - 1:
                raise
            backoff = backoff_factor * (2 ** i)
            time.sleep(backoff)


def get_friends(user_id: int, fields: str = '') -> List[Any]:
    """ Вернуть данные о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': config.VK_CONFIG.get('access_token'),
        'user_id': user_id,
        'fields': fields,
        'v': config.VK_CONFIG.get('version')
    }
    url = "{}/friends.get".format(config.VK_CONFIG.get('domain'))
    friends = get(url, query_params)
    print(friends)
    time.sleep(0.333334)
    return friends.json()



if __name__ == '__main__':
    print(get_friends(78105353,'bdate'))
