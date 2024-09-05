"""Units and conversion from default imperial system."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TemperatureUnit(Enum):
    """Temperature unit."""

    CELSIUS = 1  #: Degree Celsius °C
    FAHRENHEIT = 2  #: Degree Fahrenheit °F


class PressureUnit(Enum):
    """Pressure unit for barometric sensor values."""

    HECTOPASCAL = 1  #: Hecto-pascal hPa
    INCH_MERCURY = 2  #: Inches of mercury in Hg


class RainUnit(Enum):
    """Rain quantity unit."""

    MILLIMETER = 1  #: Millimeter mm
    INCH = 2  #: Inch


class WindSpeedUnit(Enum):
    """Wind speed unit."""

    METER_PER_SECOND = 1  #: Meter per seconds m/s
    MILES_PER_HOUR = 2  #: Miles per hour mi/h


@dataclass
class Units:
    """Units for conditions (defaults: imperial system)."""

    temperature: TemperatureUnit = TemperatureUnit.FAHRENHEIT  #: Temperature unit
    pressure: PressureUnit = PressureUnit.INCH_MERCURY  #: Pressure unit
    rain: RainUnit = RainUnit.INCH  #: Rain unit
    wind_speed: WindSpeedUnit = WindSpeedUnit.MILES_PER_HOUR  #: Wind speed unit


def convert_temperature(fahrenheit: float | None, unit: TemperatureUnit) -> float | None:
    """Convert imperial temperature (Fahrenheit) to selected unit."""
    if fahrenheit is None:
        return None
    if unit == TemperatureUnit.CELSIUS:
        return (fahrenheit - 32) * 5 / 9
    return fahrenheit


def convert_pressure(inhg: float | None, unit: PressureUnit) -> float | None:
    """Convert imperial pressure (inches of mercury) to selected unit."""
    if inhg is None:
        return None
    if unit == PressureUnit.HECTOPASCAL:
        return inhg * 33.86389
    return inhg


def convert_rain(inch: float | None, unit: RainUnit) -> float | None:
    """Convert imperial rain amount (inch) to selected unit."""
    if inch is None:
        return None
    if unit == RainUnit.MILLIMETER:
        return inch * 25.4
    return inch


def convert_wind_speed(mph: float | None, unit: WindSpeedUnit) -> float | None:
    """Convert imperial wind speed (miles per hour) to selected unit."""
    if mph is None:
        return None
    if unit == WindSpeedUnit.METER_PER_SECOND:
        return mph * 0.44704
    return mph
