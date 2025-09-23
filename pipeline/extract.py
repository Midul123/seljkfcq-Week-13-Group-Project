'''Extracts plant data from an api endpoint'''
import json
import logging
import requests


def get_plant_by_id(plant_id):
    """Gets plant data by id"""
    url = f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}"
    return requests.request(url=url, method='GET', timeout=5)


def loop_plants_api(max_attempts: int = 100, max_404_in_row: int = 5):
    """Gets the plant data and appends it to a list, loops stops after n 404s"""
    count = 0
    plants = []
    for i in range(max_attempts):
        req = get_plant_by_id(i)

        if req.status_code == 404:
            count += 1
            if count == max_404_in_row:
                logging.info(
                    f"{max_404_in_row} consecutive 404s. Stopping at iteration {i}.")
                break
        if req.status_code == 200:
            count = 0
            plants.append(req.json())
    return plants


def load_data_to_json(plants_data: list):
    """Makes a folder and adds the plant data to it in json"""
    with open('plants.json', 'w') as f:
        json.dump(plants_data, f, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    plant_data = loop_plants_api()
    load_data_to_json(plant_data)
