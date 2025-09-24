'''Extracts plant data from an api endpoint'''
import json
import logging
import requests
import aiohttp
import asyncio


async def get_plant_by_id(session, plant_id):
    """Gets plant data by id"""
    url = f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()


async def loop_plants_api(session, max_attempts: int = 70):
    """Gets the plant data and appends it to a list, loops stops after n 404s"""
    plants = []
    for i in range(max_attempts):
        task = asyncio.create_task(get_plant_by_id(session, i))
        plants.append(task)
    result = await asyncio.gather(*plants)
    return result


async def main():
    async with aiohttp.ClientSession() as session:
        data = await loop_plants_api(session)
        return data


def load_data_to_json(plants_data: list):
    """Makes a folder and adds the plant data to it in json"""
    with open('plants.json', 'w') as f:
        json.dump(plants_data, f, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    plant_data = asyncio.run(main())
    plant_data = [x for x in plant_data if x is not None]
    load_data_to_json(plant_data)
