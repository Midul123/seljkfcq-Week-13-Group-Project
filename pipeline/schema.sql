-- This file should contain all code required to create & seed database tables.

-- Create database
-- CREATE DATABASE plant_readings;

-- Drop database
-- DROP DATABASE plant_readings;

-- Drops all tables to reset database
DROP TABLE IF EXISTS botanist, city, plant, plant_reading;

-- Botanist Table
CREATE TABLE IF NOT EXISTS botanist(
    botanist_id SERIAL PRIMARY KEY,
    botanist_name VARCHAR(100) NOT NULL,
    botanist_email VARCHAR(100) NOT NULL,
    botanist_phone VARCHAR(20) NOT NULL
);

-- City Table
CREATE TABLE IF NOT EXISTS city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(100) NOT NULL
);

-- Plant Table
CREATE TABLE IF NOT EXISTS plant (
    plant_id SERIAL PRIMARY KEY,
    plant_name VARCHAR(100) NOT NULL,
    lat FLOAT NOT NULL,
    lang FLOAT NOT NULL,
    city_id INTEGER NOT NULL REFERENCES city(city_id),
    scientific_name VARCHAR(100)
);


-- Plant Reading table
CREATE TABLE IF NOT EXISTS plant_reading (
    reading_id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plant(plant_id),
    botanist_id INTEGER NOT NULL REFERENCES botanist(botanist_id),
    temperature INTEGER NOT NULL,
    last_watered TIMESTAMPTZ NOT NULL,
    soil_moisture FLOAT NOT NULL,
    recording_taken TIMESTAMPTZ NOT NULL
);