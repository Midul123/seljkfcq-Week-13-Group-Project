"""Tests for ETL pipeline functions."""

import pytest
from unittest.mock import AsyncMock

import pandas as pd
import asyncio
import pytest_asyncio

from extract import get_plant_by_id
from transform import add_columns, drop_unneeded_columns


example_data = [
    {
        "plant_id": 1,
        "name": "Venus flytrap",
        "temperature": 15,
        "origin_location":
        {
            "latitude": 43.74,
            "longitude": -11.5098,
            "city": "Stammside",
            "country": "Albania"
        },
        "botanist":
        {
            "name": "Kenneth Buckridge",
            "email": "kenneth.buckridge@lnhm.co.uk",
            "phone": "763.914.8635 x57724"
        },
        "images": {},
        "last_watered": "2025-09-24T13:51:41.000Z",
        "soil_moisture": 20,
        "recording_taken": "2025-09-25T12:29:25.400Z"
    }
]

expected_output = {
    "plant_id": 1,
    "name": "Venus flytrap",
    "temperature": 15,
    "origin_location":
    {
        "latitude": 43.74,
        "longitude": -11.5098,
        "city": "Stammside",
        "country": "Albania"
    },
    "botanist":
    {
        "name": "Kenneth Buckridge",
        "email": "kenneth.buckridge@lnhm.co.uk",
        "phone": "763.914.8635 x57724"
    },
    "images": {},
    "last_watered": "2025-09-24T13:51:41.000Z",
    "soil_moisture": 20,
    "recording_taken": "2025-09-25T12:29:25.400Z",
    "lat": 43.74,
    "long": -11.5098,
    "city": "Stammside",
    "country": "Albania",
    "botanist_name": "Kenneth Buckridge",
    "email": "kenneth.buckridge@lnhm.co.uk",
    "phone": "763.914.8635 x57724"
}


# Tests for Extract script


@pytest.mark.asyncio
async def test_valid_API_data(mocker):
    """Test valid API endpoint returns data."""

    mock_response = example_data
    mocker.patch.object("get_plant_by_id",
                        AsyncMock(return_value=mock_response))

    plant_data = await get_plant_by_id("", 1)

    assert plant_data["status"] == 200
    assert plant_data["plant_id"] == 1


# Tests for Transform script


def test_extract_plant_data_into_columns():
    """Test add_columns with a complete dictionary of test data."""

    data = pd.DataFrame.from_dict(example_data)
    df = add_columns(data)

    assert {"lat", "long", "city", "country",
            "botanist_name", "email", "phone"}.issubset(df.columns)


def test_remove_unneeded_columns():
    """Test drop_unneeded_columns with a complete dictionary of test data."""

    data = pd.DataFrame.from_dict(example_data)
    df = drop_unneeded_columns(data)

    assert not {"origin_location", "botanist", "images"}.issubset(df.columns)
