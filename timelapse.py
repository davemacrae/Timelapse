#!/usr/bin/env python

from sun import get_sun_position
import datetime

if __name__ == "__main__":
    city_name = "Edinburgh"
    date_time = datetime.date(2025, 12, 21)
    sun_position = get_sun_position(city_name, date_time)
    print(f"Sun position in {city_name} on {date_time}:")
    print(f"Sunrise: {sun_position['sunrise']}")
    print(f"Sunset: {sun_position['sunset']}")