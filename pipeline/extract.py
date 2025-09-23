import requests
import json
import logging


def loop_plants_api():
    count = 0
    plants = []
    for i in range(1000):
        num = i
        url = f"https://sigma-labs-bot.herokuapp.com/api/plants/{num}"
        req = requests.request(url=url, method='GET')
        if req.status_code == 404:
            count += 1
            if count == 5:
                logging.info(
                    f"5 status code 404's in a row stopping loop! iteration {i}")
                break
        if req.status_code == 200:
            count = 0
            plants.append(req.json())
    return plants


def load_data_to_json(plants_data: list):
    with open('plants.json', 'w') as f:
        json.dump(plants_data, f, indent=4)


if __name__ == "__main__":
    plants = loop_plants_api()
    load_data_to_json(plants)
