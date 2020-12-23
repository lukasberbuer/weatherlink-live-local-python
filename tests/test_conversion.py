import pytest

import weatherlink_live_local as wlll

RTOL = 0.001


@pytest.mark.parametrize(
    "raw, fahrenheit, celsius", (
        (0, 0, -17.7778),
        (32, 32, 0),
    )
)
def test_convert_temperature(raw, fahrenheit, celsius):
    wlll.set_units(temperature=wlll.units.TemperatureUnit.FAHRENHEIT)
    assert wlll.units.convert_temperature(raw) == fahrenheit
    wlll.set_units(temperature=wlll.units.TemperatureUnit.CELSIUS)
    assert wlll.units.convert_temperature(raw) == pytest.approx(celsius, rel=RTOL)


@pytest.mark.parametrize(
    "raw, inhg, hpa", (
        (0, 0, 0),
        (1, 1, 33.86),
    )
)
def test_convert_pressure(raw, inhg, hpa):
    wlll.set_units(pressure=wlll.units.PressureUnit.INCH_MERCURY)
    assert wlll.units.convert_pressure(raw) == inhg
    wlll.set_units(pressure=wlll.units.PressureUnit.HECTOPASCAL)
    assert wlll.units.convert_pressure(raw) == pytest.approx(hpa, rel=RTOL)


@pytest.mark.parametrize(
    "raw, mph, ms", (
        (0, 0, 0),
        (1, 1, 0.44704),
    )
)
def test_convert_wind_speed(raw, mph, ms):
    wlll.set_units(wind_speed=wlll.units.WindSpeedUnit.MILES_PER_HOUR)
    assert wlll.units.convert_wind_speed(raw) == mph
    wlll.set_units(wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND)
    assert wlll.units.convert_wind_speed(raw) == pytest.approx(ms, rel=RTOL)
