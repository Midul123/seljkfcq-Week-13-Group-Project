"""Extracts plant data from an api endpoint"""

import os
import logging
import json

import aiohttp
import asyncio

from utils import setup_logging, check_for_tmp_folder


async def get_plant_by_id(session: aiohttp.ClientSession, plant_id: int) -> json:
    """Get plant data from API endpoint."""

    url = f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}"

    async with session.get(url) as response:
        if response.status == 200:
            logging.info("Connected to API plant endpoint")
            return await response.json()

    logging.error("API endpoint for plant does not exist")


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


def load_data_to_json(plant_data: list) -> None:
    """Add plant data to temporary folder as a JSON file."""

    check_for_tmp_folder()
    file_path = "/tmp/plants.json"
    with open(file_path, 'w') as f:
        json.dump(plant_data, f, indent=4)
    logging.info(f"Created JSON file to store plant data: {file_path}")


def run_extract() -> None:
    """Runs the complete Extract script."""

    plant_data = asyncio.run(async_main())
    plant_data = drop_null_plants(plant_data)
    load_data_to_json(plant_data)
    logging.info("Extract script run successfully")


if __name__ == "__main__":
    setup_logging()
    run_extract()
