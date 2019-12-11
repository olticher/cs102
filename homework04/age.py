import datetime
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User

def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    current = datetime.datetime.now()
    data = get_friends(user_id, 'bdate')
    ages = []
    for i in range(0, len(data['response']['items'])):
    	try:
    		bdate = data['response']['items'][i]['bdate']
    		if len(bdate) > 6:
    			day, month, year = bdate.split('.')
    			day = int(day)
    			month = int(month)
    			year = int(year)
    		else:
    			continue
    		date_bdate = current.replace(year = year, month = month, day = day)
    		age = current - date_bdate
    		ages.append(age.days // 365)
    	except:
    		pass

    return median(ages)

if __name__ == '__main__':
	print(age_predict(32706804))
