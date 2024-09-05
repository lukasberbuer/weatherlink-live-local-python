import pytest

from weatherlink_live_local.units import (
    PressureUnit,
    RainUnit,
    TemperatureUnit,
    WindSpeedUnit,
    convert_pressure,
    convert_rain,
    convert_temperature,
    convert_wind_speed,
)

RTOL = 0.001


@pytest.mark.parametrize(
    ("raw", "fahrenheit", "celsius"),
    [
        (0, 0, -17.7778),
        (32, 32, 0),
    ],
)
def test_convert_temperature(raw, fahrenheit, celsius):
    assert convert_temperature(raw, TemperatureUnit.FAHRENHEIT) == fahrenheit
    assert convert_temperature(raw, TemperatureUnit.CELSIUS) == pytest.approx(celsius, rel=RTOL)


@pytest.mark.parametrize(
    ("raw", "inhg", "hpa"),
    [
        (0, 0, 0),
        (1, 1, 33.86),
    ],
)
def test_convert_pressure(raw, inhg, hpa):
    assert convert_pressure(raw, PressureUnit.INCH_MERCURY) == inhg
    assert convert_pressure(raw, PressureUnit.HECTOPASCAL) == pytest.approx(hpa, rel=RTOL)


@pytest.mark.parametrize(
    ("raw", "inch", "mm"),
    [
        (0, 0, 0),
        (1, 1, 25.4),
    ],
)
def test_convert_rain(raw, inch, mm):
    assert convert_rain(raw, RainUnit.INCH) == inch
    assert convert_rain(raw, RainUnit.MILLIMETER) == pytest.approx(mm, rel=RTOL)


@pytest.mark.parametrize(
    ("raw", "mph", "ms"),
    [
        (0, 0, 0),
        (1, 1, 0.44704),
    ],
)
def test_convert_wind_speed(raw, mph, ms):
    assert convert_wind_speed(raw, WindSpeedUnit.MILES_PER_HOUR) == mph
    assert convert_wind_speed(raw, WindSpeedUnit.METER_PER_SECOND) == pytest.approx(ms, rel=RTOL)
