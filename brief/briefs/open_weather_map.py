"""
Open Weather Map

This requires an API Key and a city id as environment variables:

api = os.environ.get("BRIEF_OWM_API_KEY")
city_id = os.environ.get("BRIEF_OWM_CITY_ID", "44333669")  # Monroe, LA, US
units = os.environ.get("BRIEF_OWM_UNITS", "imperial")

For temperature in Fahrenheit use units=imperial
For temperature in Celsius use units=metric
Temperature in Kelvin is used by default, no need to use units parameter in API call


Example return data:
{
    "coord": {"lon": -92.15, "lat": 32.52},
    "weather": [
        {"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}
    ],
    "base": "stations",
    "main": {
        "temp": 44.73,
        "feels_like": 38.43,
        "temp_min": 42.8,
        "temp_max": 46.99,
        "pressure": 1024,
        "humidity": 70,
    },
    "visibility": 16093,
    "wind": {"speed": 5.82, "deg": 20},
    "clouds": {"all": 1},
    "dt": 1586924552,
    "sys": {
        "type": 1,
        "id": 4932,
        "country": "US",
        "sunrise": 1586864373,
        "sunset": 1586911048,
    },
    "timezone": -18000,
    "id": 4345850,
    "name": "West Monroe",
    "cod": 200,
}
"""
import logging
import os

from typing import Dict

from aiohttp import ClientSession

from brief.utils.decorators import ATimedMemo


name = "open_weather_map"
logger = logging.getLogger(__name__)


@ATimedMemo(minutes=10)  # owm suggests a 10 minute cache
async def get_weather(
    city_id: str, api_key: str, units: str, session: ClientSession
) -> Dict:
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
    )
    if units:
        url += f"&units={units}"
    async with session.get(url) as resp:
        if resp.status == 200:
            data = resp.json()
            return await data
        if resp.status == 401:
            raise ValueError(
                f"Likely missing or incorrect api key: {await resp.text()}"
            )
        if resp.status == 404:
            raise ValueError(f"OWM request failed, probably invalid city id: {city_id}")
        raise ValueError(f"OWM request failed. {resp.status}: {await resp.text()}")


async def run_brief(session: ClientSession):
    try:
        api_key = os.environ["BRIEF_OWM_API_KEY"]
    except KeyError:
        logger.error("No OpenWeatherMap API Key")
        raise KeyError("No OpenWeatherMap API Key, set BRIEF_OWM_API_KEY variable")

    city_id = os.environ.get("BRIEF_OWM_CITY_ID", "4333669")  # Monroe, LA, US
    units = os.environ.get("BRIEF_OWM_UNITS", "imperial")
    weather = await get_weather(
        city_id, api_key, units, session
    )  # trying to call a coroutine?
    return weather
