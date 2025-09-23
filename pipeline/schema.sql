-- This file should contain all code required to create & seed database tables.

-- Drops all tables to reset database

IF OBJECT_ID('gamma.plant_reading', 'U') IS NOT NULL
    DROP TABLE gamma.plant_reading

IF OBJECT_ID('gamma.plant', 'U') IS NOT NULL
    DROP TABLE gamma.plant

IF OBJECT_ID('gamma.botanist', 'U') IS NOT NULL
    DROP TABLE gamma.botanist

IF OBJECT_ID('gamma.city', 'U') IS NOT NULL
    DROP TABLE gamma.city


-- Creates Botanist Table
CREATE TABLE gamma.botanist(
    botanist_id INT IDENTITY(1,1) PRIMARY KEY,
    botanist_name VARCHAR(100) NOT NULL,
    botanist_email VARCHAR(100) NOT NULL,
    botanist_phone VARCHAR(20) NOT NULL,
);

-- Creates City Table
CREATE TABLE gamma.city (
    city_id INT IDENTITY(1,1) PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(100) NOT NULL
);

-- Creates Plant Table
CREATE TABLE gamma.plant (
    plant_id INT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(100) NOT NULL,
    lat FLOAT NOT NULL,
    lang FLOAT NOT NULL,
    city_id INTEGER NOT NULL REFERENCES city(city_id),
    scientific_name VARCHAR(100)
);


-- Creates Plant Reading table
CREATE TABLE gamma.plant_reading (
    reading_id INT IDENTITY(1,1) PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plant(plant_id),
    botanist_id INTEGER NOT NULL REFERENCES botanist(botanist_id),
    temperature INTEGER NOT NULL,
    last_watered DATETIME2 NOT NULL,
    soil_moisture FLOAT NOT NULL,
    recording_taken DATETIME2 NOT NULL
);