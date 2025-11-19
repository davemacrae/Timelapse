#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module: sun
Description: This module provides functions to calculate the position of the sun
             based on date, time, and geographic location.
"""
import astral
from astral import LocationInfo
from astral.geocoder import lookup, database
from astral.sun import sun

import datetime

def get_sun_position(city_name, date_time=None):
    """
    Calculate the position of the sun for a given city and date/time.

    :param city_name: Name of the city (must be in the astral database)
    :param date_time: datetime object representing the date and time (default is now)
    :return: Dictionary with sun position details (azimuth, elevation, sunrise, sunset)
    """
    
    if date_time is None:
        date_time = datetime.datetime.now()

    try:
        city_data: LocationInfo = lookup(city_name, database()) # type: ignore
    except KeyError:
        raise ValueError(f"City '{city_name}' not found in the astral database.")

    city = LocationInfo(name=city_data.name, 
                        region=city_data.region, 
                        timezone=city_data.timezone,
                        latitude=city_data.latitude, 
                        longitude=city_data.longitude)
    my_sun = sun(city.observer, date=date_time)

    return {
        'sunrise': my_sun['sunrise'],
        'sunset': my_sun['sunset']
    }

if __name__ == "__main__":
    city_name = "Edinburgh"
    date_time = datetime.date(2025, 12, 21)
    sun_position = get_sun_position(city_name, date_time)
    print(f"Sun position in {city_name} on {date_time}:")
    print(f"Sunrise: {sun_position['sunrise']}")
    print(f"Sunset: {sun_position['sunset']}")