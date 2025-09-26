"""Script to extract plant data from an API endpoint."""

import logging
import json

import aiohttp
import asyncio

from utils import setup_logging, check_for_tmp_folder


async def get_plant_by_id(session: aiohttp.ClientSession, plant_id: int) -> json:
    """Get plant data from API endpoint."""

    url = f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}"
    tries = 0
    max_retries = 4

    while tries < max_retries:
        async with session.get(url) as response:
            if response.status == 200:
                logging.info(f"Connected to API plant endpoint: {plant_id}")
                return await response.json()

            if response.status == 404:
                logging.error(
                    f"ERROR 404: API endpoint for plant does not exist: {plant_id}")
                break

            if response.status == 500:
                tries += 1
                logging.error(
                    f"ERROR 500: Could not connect to API server for endpoint: {plant_id}")


async def loop_plants_api(session: aiohttp.ClientSession, max_attempts: int = 70) -> list:
    """
    Get plant data and append it to a list.
    Loop stops after specified number of endpoints are retrieved.
    """

    plants = []
    for i in range(max_attempts):
        task = asyncio.create_task(get_plant_by_id(session, i))
        plants.append(task)

    result = await asyncio.gather(*plants)
    logging.info("Retrieved plant data")
    return result


async def async_main() -> list:
    """Async session to retrieve plant data."""

    async with aiohttp.ClientSession() as session:
        data = await loop_plants_api(session)
        return data


def drop_null_plants(plant_data: list) -> list:
    """Drops null values from retrieved plant data."""

    plant_data = [x for x in plant_data if x is not None]
    logging.info("IDs without plant recordings dropped")
    return plant_data


def save_data_as_json(plant_data: list) -> None:
    """Add plants data to temporary folder as a JSON file."""

    check_for_tmp_folder()
    with open('/tmp/plants.json', 'w') as f:
        json.dump(plant_data, f, indent=4)
    logging.info("Created JSON file to store plant data: /tmp/plants.json")


def run_extract() -> None:
    """Run extract script."""

    plant_data = asyncio.run(async_main())
    plant_data = drop_null_plants(plant_data)
    save_data_as_json(plant_data)
    logging.info("Extract script run successfully")


if __name__ == "__main__":
    setup_logging()
    run_extract()
