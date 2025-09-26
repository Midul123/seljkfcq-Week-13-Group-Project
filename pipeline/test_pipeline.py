"""Tests for ETL pipeline functions."""

# pylint: skip-file

import pytest

import pandas as pd

from transform import (add_columns, drop_unneeded_columns, clean_phone_numbers,
                       remove_brackets_from_scientific_name, clean_emails)


example_data = [
    {
        "plant_id": 1,
        "name": "Venus flytrap",
        "temperature": 13.844216378124159,
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
        "soil_moisture": 39.441591985428055,
        "recording_taken": "2025-09-25T12:29:25.400Z"
    }
]


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


def test_clean_phone_numbers():
    """Test clean_phone_numbers with multiple numbers in the column."""

    data = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "phone": "763.914.8635 x57724"
        },
        {
            "plant_id": 2,
            "phone": "673.641.8851"
        }, {
            "plant_id": 3,
            "phone": "673.641.8851"
        },
        {
            "plant_id": 4,
            "phone": "1-661-425-6823 x4455"
        }
    ])

    expected_outcome = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "phone": "763-914-8635"
        },
        {
            "plant_id": 2,
            "phone": "673-641-8851"
        }, {
            "plant_id": 3,
            "phone": "673-641-8851"
        },
        {
            "plant_id": 4,
            "phone": "661-425-6823"
        }
    ])

    result = clean_phone_numbers(data)
    assert result['phone'].to_list() == expected_outcome['phone'].to_list()


def test_remove_brackets_from_scientific_name():
    """Test remove_brackets_from_scientific_name with multiple names in the column."""

    data = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "scientific_name": "[ Asclepias curassavica ]"
        },
        {
            "plant_id": 2,
            "scientific_name": "[ Hippeastrum (group) ]"
        }, {
            "plant_id": 3,
            "scientific_name": "[ Chlorophytum comosum 'Vittatum' ]"
        }
    ])

    expected_outcome = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "scientific_name": " Asclepias curassavica "
        },
        {
            "plant_id": 2,
            "scientific_name": " Hippeastrum (group) "
        }, {
            "plant_id": 3,
            "scientific_name": " Chlorophytum comosum 'Vittatum' "
        }
    ])

    result = remove_brackets_from_scientific_name(data)
    assert result['scientific_name'].to_list(
    ) == expected_outcome['scientific_name'].to_list()


def test_clean_emails():
    """Test clean_emails with multiple emails in the column."""

    data = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "email": "kenneth.buckridge@lnhm.co.uk"
        },
        {
            "plant_id": 2,
            "email": "ms..diana.king@lnhm.co.uk"
        }, {
            "plant_id": 3,
            "email": "irma.ortiz.jr.@lnhm.co.uk"
        },
        {
            "plant_id": 4,
            "email": "oscar.schinner-little@lnhm.co.uk"
        }
    ])

    expected_outcome = pd.DataFrame.from_dict([
        {
            "plant_id": 1,
            "email": "kenneth.buckridge@lnhm.co.uk"
        },
        {
            "plant_id": 2,
            "email": "ms.diana.king@lnhm.co.uk"
        }, {
            "plant_id": 3,
            "email": "irma.ortiz.jr@lnhm.co.uk"
        },
        {
            "plant_id": 4,
            "email": "oscar.schinner-little@lnhm.co.uk"
        }
    ])

    result = clean_emails(data)
    assert result['email'].to_list() == expected_outcome['email'].to_list()
