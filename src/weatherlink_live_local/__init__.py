"""WeatherLink Live Local Python API."""

import json
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, List, NamedTuple, Optional

from . import units
from .conditions import *
from .discovery import Discovery, ServiceInfo


def discover(timeout: int = 1) -> List[ServiceInfo]:
    """
    Discover all WeatherLink Live services on local network(s).

    Args:
        timeout: Timeout in seconds

    Returns:
        List of found services
    """
    return Discovery.find(timeout=timeout)


def get_conditions(ip: str, port: int = 80, timeout: int = 1) -> Conditions:
    """
    Read conditions from WeatherLink Live device + all connected sensors.

    Args:
        ip: IP address of WeatherLink Live device.
            Use `discover` function to find devices with their IP address in the local network.
        port: Port number of HTTP interface, should be 80
        timeout: Maximum time to listen for WeatherLink Live services

    Returns:
        Conditions of all available sensors
    """

    with urllib.request.urlopen(
        f"http://{ip}:{port}/v1/current_conditions",
        timeout=timeout,
    ) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP response code {resp.status}")

        content = json.loads(resp.read().decode("utf-8"))
        json_data = content["data"]

        def conditions_by_type(type_: int):
            return filter(
                lambda c: c["data_structure_type"] == type_,
                json_data["conditions"],
            )

        return Conditions(
            timestamp=datetime.fromtimestamp(json_data["ts"]),
            inside=InsideConditions.from_dict(next(conditions_by_type(4))),
            barometric=BarometricConditions.from_dict(next(conditions_by_type(3))),
            moisture_temperature_stations=[
                MoistureTemperatureConditions.from_dict(c) for c in conditions_by_type(2)
            ],
            integrated_sensor_suites=[
                SensorSuiteConditions.from_dict(c) for c in conditions_by_type(1)
            ],
        )


def set_units(
    temperature: Optional[units.TemperatureUnit] = None,
    pressure: Optional[units.PressureUnit] = None,
    rain: Optional[units.RainUnit] = None,
    wind_speed: Optional[units.WindSpeedUnit] = None,
):
    """
    Set desired units for `get_conditions` command.

    Args:
        temperature: Temperature unit
        pressure: Pressure unit
        rain: Rain amount unit
        wind_speed: Wind speed unit

    Example:
        >>> import weatherlink_live_local as wlll
        >>> # change only a single unit
        >>> wlll.set_units(temperature=wlll.units.TemperatureUnit.CELSIUS)
        >>> # change multiple units at once
        >>> wlll.set_units(
        >>>     pressure=wlll.units.PressureUnit.HECTOPASCAL,
        >>>     rain=wlll.units.RainUnit.MILLIMETER,
        >>> )
    """
    if temperature is not None:
        units.UNITS["temperature"] = temperature
    if pressure is not None:
        units.UNITS["pressure"] = pressure
    if rain is not None:
        units.UNITS["rain"] = rain
    if wind_speed is not None:
        units.UNITS["wind_speed"] = wind_speed
