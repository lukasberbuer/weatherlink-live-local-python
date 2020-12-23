"""Units and conversion from default imperial system."""

from enum import Enum
from typing import Optional


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


# store selected units and set defaults
UNITS = dict(
    temperature=TemperatureUnit.FAHRENHEIT,
    pressure=PressureUnit.INCH_MERCURY,
    rain=RainUnit.INCH,
    wind_speed=WindSpeedUnit.MILES_PER_HOUR,
)


def convert_temperature(fahrenheit: Optional[float]) -> Optional[float]:
    """Convert imperial temperature (Fahrenheit) to selected unit."""
    if fahrenheit is None:
        return None
    unit = UNITS["temperature"]
    if unit == TemperatureUnit.CELSIUS:
        return (fahrenheit - 32) * 5 / 9
    if unit == TemperatureUnit.FAHRENHEIT:
        return fahrenheit
    raise ValueError(f"Invalid temperature unit '{unit}'")


def convert_pressure(inhg: Optional[float]) -> Optional[float]:
    """Convert imperial pressure (inches of mercury) to selected unit."""
    if inhg is None:
        return None
    unit = UNITS["pressure"]
    if unit == PressureUnit.HECTOPASCAL:
        return inhg * 33.86389
    if unit == PressureUnit.INCH_MERCURY:
        return inhg
    raise ValueError(f"Invalid pressure unit '{unit}'")


def convert_rain(inch: Optional[float]) -> Optional[float]:
    """Convert imperial rain amount (inch) to selected unit."""
    if inch is None:
        return None
    unit = UNITS["rain"]
    if unit == RainUnit.INCH:
        return inch
    if unit == RainUnit.MILLIMETER:
        return inch * 25.4
    raise ValueError(f"Invalid rain unit '{unit}'")


def convert_wind_speed(mph: Optional[float]) -> Optional[float]:
    """Convert imperial wind speed (miles per hour) to selected unit."""
    if mph is None:
        return None
    unit = UNITS["wind_speed"]
    if unit == WindSpeedUnit.MILES_PER_HOUR:
        return mph
    if unit == WindSpeedUnit.METER_PER_SECOND:
        return mph * 0.44704
    raise ValueError(f"Invalid wind speed unit '{unit}'")
