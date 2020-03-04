import requests
import time


def get(url, params={}, timeout=500, max_retries=10, backoff_factor=0.3):

    try:
        response = requests.get(url, timeout=timeout)
        return response
    except requests.exceptions.RequestException as re_err:
        for i in range(max_retries - 1):
            try:
                delay = backoff_factor * (2 ** i)
                time.sleep(delay)
                response = requests.get(url)
                return response
            except requests.exceptions.RequestException:
                continue
        raise re_err
    except requests.exceptions.ConnectionError as c_err:
        raise c_err
    except requests.exceptions.HTTPError as http_err:
        raise http_err
    except requests.exceptions.ReadTimeout as rt_err:
        raise rt_err
