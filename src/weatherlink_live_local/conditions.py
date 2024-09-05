"""Datatypes to gather device-specific sensor data / conditions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any

from weatherlink_live_local.units import (
    Units,
    convert_pressure,
    convert_rain,
    convert_temperature,
    convert_wind_speed,
)

# fmt: off

class DataStructureType(IntEnum):
    """Data structure type to differentiate condition types."""

    SENSOR_SUITE = 1
    MOISTURE_TEMPERATURE = 2
    BAROMETRIC = 3
    INSIDE = 4


@dataclass
class _SensorIdentifier:
    """Sensor identifier used by all *Condition classes."""

    lsid: int  #: Logical sensor ID

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):  # noqa: ARG003
        return cls(lsid=json_data["lsid"])


class RadioReceptionState(IntEnum):
    """Transmitter radio reception state."""

    SYNCED_TRACKING = 0  #: Transmitter has been acquired and is actively being received
    SYNCED = 1  #: Transmitter has been acquired, but we have missed 1-14 packets in a row
    SCANNING = 2  #: Transmitter has not been acquired yet, or we've lost it (more than 15 missed packets in a row)


@dataclass
class _WirelessSensorUnit:
    """Wireless sensor unit information."""

    txid: int  #: Transmitter ID
    rx_state: RadioReceptionState | None  #: Radio reception state
    trans_battery_flag: int  #: Transmitter battery flag

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):  # noqa: ARG003
        return cls(
            txid=json_data["txid"],
            rx_state=(
                None if json_data["rx_state"] is None
                else RadioReceptionState(json_data["rx_state"])
            ),
            trans_battery_flag=json_data["trans_battery_flag"],
        )


@dataclass
class SensorSuiteConditions(_SensorIdentifier, _WirelessSensorUnit):
    """
    Conditions of integrated sensor suite (ISS), e.g. Vantage Vue.

    Data structure for `data_structure_type = DataStructureType.SENSOR_SUITE`
    """

    temp: float | None  #: Temperature [`TemperatureUnit`]
    hum: float | None  #: Humidity [%]
    dew_point: float | None  #: Dew point [`TemperatureUnit`]
    wet_bulb: float | None  #: Wet bulb [`TemperatureUnit`]
    heat_index: float | None  #: Heat index [`TemperatureUnit`]
    wind_chill: float | None  #: Wind chill [`TemperatureUnit`]
    thw_index: float | None  #: THW index [`TemperatureUnit`]
    thsw_index: float | None  #: THSW index [`TemperatureUnit`]

    wind_speed_last: float | None  #: Most recent wind speed [`WindSpeedUnit`]
    wind_speed_avg_last_1_min: float | None  #: Average wind speed over last 1 min [`WindSpeedUnit`]
    wind_speed_avg_last_2_min: float | None  #: Average wind speed over last 2 min [`WindSpeedUnit`]
    wind_speed_avg_last_10_min: float | None  #: Average wind speed over last 10 min [`WindSpeedUnit`]
    wind_speed_hi_last_2_min: float | None  #: Maximum wind speed over last 2 min [`WindSpeedUnit`]
    wind_speed_hi_last_10_min: float | None  #: Maximum wind speed over last 10 min [`WindSpeedUnit`]

    wind_dir_last: float | None  #: Wind direction [°]
    wind_dir_scalar_avg_last_1_min: float | None  #: Average wind direction over last 1 min [°]
    wind_dir_scalar_avg_last_2_min: float | None  #: Average wind direction over last 2 min [°]
    wind_dir_scalar_avg_last_10_min: float | None  #: Average wind direction over last 10 min [°]
    wind_dir_at_hi_speed_last_2_min: float | None  #: Gust wind direction over last 2 min [°]
    wind_dir_at_hi_speed_last_10_min: float | None  #: Gust wind direction over last 10 min [°]

    rainfall_last_60_min: float | None  #: Total rain for last 60 min [`RainUnit`]
    rainfall_last_24_hr: float | None  #: Total rain for last 24 hours [`RainUnit`]
    rainfall_daily: float | None  #: Total rain since local midnight [`RainUnit`]
    rainfall_monthly: float | None  #: Total rain since first of month [`RainUnit`]
    rainfall_year: float | None  #: Total rain since first of user-chosen month at local midnight [`RainUnit`]

    rain_rate_last: float | None  #: Rain rate [`RainUnit`/hour]
    rain_rate_hi_last_1_min: float | None  #: Highest rain rate over last 1 min [`RainUnit`/hour]
    rain_rate_hi_last_15_min: float | None  #: Highest rain rate over last 15 min [`RainUnit`/hour]

    rain_storm_last: float | None  #: Total rain since last 24 hour long break in rain [`RainUnit`]
    rain_storm_last_start_at: datetime | None  #: Timestamp of last rain storm start
    rain_storm_last_end_at: datetime | None  #: Timestamp of last rain storm start

    solar_rad: float | None  #: Solar radiation [W/m²]
    uv_index: float | None  #: UV index

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):
        rain_size_inches = {
            1: 0.01,  # 0.01"
            2: 0.2 / 25.4,  # 0.2 mm
            3: 0.1 / 25.4,  # 0.1 mm
            4: 0.001,  # 0.001"
        }[json_data["rain_size"]]

        def counts_to_inch(counts: int | None) -> float | None:
            if counts is None:
                return None
            return counts * rain_size_inches

        def to_datetime(timestamp: int | None) -> datetime | None:
            if timestamp is None:
                return None
            return datetime.fromtimestamp(timestamp, timezone.utc)

        assert json_data["data_structure_type"] == DataStructureType.SENSOR_SUITE
        return cls(
            **asdict(_SensorIdentifier.from_dict(json_data, units)),
            **asdict(_WirelessSensorUnit.from_dict(json_data, units)),
            temp=convert_temperature(json_data["temp"], units.temperature),
            hum=json_data["hum"],
            dew_point=convert_temperature(json_data["dew_point"], units.temperature),
            wet_bulb=convert_temperature(json_data["wet_bulb"], units.temperature),
            heat_index=convert_temperature(json_data["heat_index"], units.temperature),
            wind_chill=convert_temperature(json_data["wind_chill"], units.temperature),
            thw_index=convert_temperature(json_data["thw_index"], units.temperature),
            thsw_index=convert_temperature(json_data["thsw_index"], units.temperature),

            wind_speed_last=convert_wind_speed(json_data["wind_speed_last"], units.wind_speed),
            wind_speed_avg_last_1_min=convert_wind_speed(json_data["wind_speed_avg_last_1_min"], units.wind_speed),
            wind_speed_avg_last_2_min=convert_wind_speed(json_data["wind_speed_avg_last_2_min"], units.wind_speed),
            wind_speed_avg_last_10_min=convert_wind_speed(json_data["wind_speed_avg_last_10_min"], units.wind_speed),
            wind_speed_hi_last_2_min=convert_wind_speed(json_data["wind_speed_hi_last_2_min"], units.wind_speed),
            wind_speed_hi_last_10_min=convert_wind_speed(json_data["wind_speed_hi_last_10_min"], units.wind_speed),

            wind_dir_last=json_data["wind_dir_last"],
            wind_dir_scalar_avg_last_1_min=json_data["wind_dir_scalar_avg_last_1_min"],
            wind_dir_scalar_avg_last_2_min=json_data["wind_dir_scalar_avg_last_2_min"],
            wind_dir_scalar_avg_last_10_min=json_data["wind_dir_scalar_avg_last_10_min"],
            wind_dir_at_hi_speed_last_2_min=json_data["wind_dir_at_hi_speed_last_2_min"],
            wind_dir_at_hi_speed_last_10_min=json_data["wind_dir_at_hi_speed_last_10_min"],

            rainfall_last_60_min=convert_rain(counts_to_inch(json_data["rainfall_last_60_min"]), units.rain),
            rainfall_last_24_hr=convert_rain(counts_to_inch(json_data["rainfall_last_24_hr"]), units.rain),
            rainfall_daily=convert_rain(counts_to_inch(json_data["rainfall_daily"]), units.rain),
            rainfall_monthly=convert_rain(counts_to_inch(json_data["rainfall_monthly"]), units.rain),
            rainfall_year=convert_rain(counts_to_inch(json_data["rainfall_year"]), units.rain),

            rain_rate_last=convert_rain(counts_to_inch(json_data["rain_rate_last"]), units.rain),
            rain_rate_hi_last_1_min=convert_rain(counts_to_inch(json_data["rain_rate_hi"]), units.rain),
            rain_rate_hi_last_15_min=convert_rain(counts_to_inch(json_data["rain_rate_hi_last_15_min"]), units.rain),

            rain_storm_last=convert_rain(counts_to_inch(json_data["rain_storm_last"]), units.rain),
            rain_storm_last_start_at=to_datetime(json_data["rain_storm_last_start_at"]),
            rain_storm_last_end_at=to_datetime(json_data["rain_storm_last_end_at"]),

            solar_rad=json_data["solar_rad"],
            uv_index=json_data["uv_index"],
        )


@dataclass
class MoistureTemperatureConditions(_SensorIdentifier, _WirelessSensorUnit):
    """
    Conditions of leaf & soil moisture/temperature station.

    Data structure for `data_structure_type = DataStructureType.MOISTURE_TEMPERATURE`
    """

    temp_1: float | None  #: Temperature slot 1 [`TemperatureUnit`]
    temp_2: float | None  #: Temperature slot 2 [`TemperatureUnit`]
    temp_3: float | None  #: Temperature slot 3 [`TemperatureUnit`]
    temp_4: float | None  #: Temperature slot 4 [`TemperatureUnit`]
    moist_soil_1: float | None  #: Moisture soil slot 1 [cb]
    moist_soil_2: float | None  #: Moisture soil slot 2 [cb]
    moist_soil_3: float | None  #: Moisture soil slot 3 [cb]
    moist_soil_4: float | None  #: Moisture soil slot 4 [cb]
    wet_leaf_1: float | None  #: Leaf wetness slot 1
    wet_leaf_2: float | None  #: Leaf wetness slot 2

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):
        assert json_data["data_structure_type"] == DataStructureType.MOISTURE_TEMPERATURE
        return cls(
            **asdict(_SensorIdentifier.from_dict(json_data, units)),
            **asdict(_WirelessSensorUnit.from_dict(json_data, units)),
            temp_1=convert_temperature(json_data["temp_1"], units.temperature),
            temp_2=convert_temperature(json_data["temp_2"], units.temperature),
            temp_3=convert_temperature(json_data["temp_3"], units.temperature),
            temp_4=convert_temperature(json_data["temp_4"], units.temperature),
            moist_soil_1=json_data["moist_soil_1"],
            moist_soil_2=json_data["moist_soil_2"],
            moist_soil_3=json_data["moist_soil_3"],
            moist_soil_4=json_data["moist_soil_4"],
            wet_leaf_1=json_data["wet_leaf_1"],
            wet_leaf_2=json_data["wet_leaf_2"],
        )


@dataclass
class BarometricConditions(_SensorIdentifier):
    """
    Barometric conditions of WeatherLink Live station.

    Data structure for `data_structure_type = DataStructureType.BAROMETRIC`
    """

    bar_sea_level: float | None  #: Most recent bar sensor reading with elevation adjustment [`PressureUnit`]
    bar_trend: float | None  #: Current 3 hour bar trend [`PressureUnit`]
    bar_absolute: float | None  #: Raw bar sensor reading [`PressureUnit`]

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):
        assert json_data["data_structure_type"] == DataStructureType.BAROMETRIC
        return cls(
            **asdict(_SensorIdentifier.from_dict(json_data, units)),
            bar_absolute=convert_pressure(json_data["bar_absolute"], units.pressure),
            bar_sea_level=convert_pressure(json_data["bar_sea_level"], units.pressure),
            bar_trend=convert_pressure(json_data["bar_trend"], units.pressure),
        )


@dataclass
class InsideConditions(_SensorIdentifier):
    """
    Inside conditions of WeatherLink Live station.

    Data structure for `data_structure_type = DataStructureType.INSIDE`
    """

    temp: float | None  #: Inside temperature [`TemperatureUnit`]
    hum: float | None  #: Inside humidity [%]
    dew_point: float | None  #: Dew point [`TemperatureUnit`]
    heat_index: float | None  #: Heat index [`TemperatureUnit`]

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):
        assert json_data["data_structure_type"] == DataStructureType.INSIDE
        return cls(
            **asdict(_SensorIdentifier.from_dict(json_data, units)),
            temp=convert_temperature(json_data["temp_in"], units.temperature),
            hum=json_data["hum_in"],
            dew_point=convert_temperature(json_data["dew_point_in"], units.temperature),
            heat_index=convert_temperature(json_data["heat_index_in"], units.temperature),
        )


@dataclass
class Conditions:
    """
    Gathered conditions of all available sensors.

    Returned by `parse_response` or `get_conditions` function.
    """

    timestamp: datetime  #: Timestamp
    inside: InsideConditions  #: Inside conditions of WeatherLink Live station
    barometric: BarometricConditions  #: Barometric conditions of WeatherLink Live station
    moisture_temperature_stations: list[MoistureTemperatureConditions]  #: Conditions of leaf & soil moisture/temperature station(s)
    integrated_sensor_suites: list[SensorSuiteConditions]  #: Conditions of integrated sensor suite(s), e.g. Vantage Vue

    @classmethod
    def from_dict(cls, json_data: dict[str, Any], units: Units):
        def conditions_by_type(data_structure_type: DataStructureType):
            return filter(
                lambda c: c["data_structure_type"] == data_structure_type,
                json_data["conditions"],
            )

        return cls(
            timestamp=datetime.fromtimestamp(json_data["ts"], timezone.utc),
            inside=InsideConditions.from_dict(
                next(conditions_by_type(DataStructureType.INSIDE)),
                units
            ),
            barometric=BarometricConditions.from_dict(
                next(conditions_by_type(DataStructureType.BAROMETRIC)),
                units
            ),
            moisture_temperature_stations=[
                MoistureTemperatureConditions.from_dict(c, units)
                for c in conditions_by_type(DataStructureType.MOISTURE_TEMPERATURE)
            ],
            integrated_sensor_suites=[
                SensorSuiteConditions.from_dict(c, units)
                for c in conditions_by_type(DataStructureType.SENSOR_SUITE)
            ],
        )
