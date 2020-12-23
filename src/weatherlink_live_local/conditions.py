"""Datatypes to gather device-specific sensor data / conditions."""

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, List, Optional

from .units import convert_pressure, convert_rain, convert_temperature, convert_wind_speed

# fmt: off
# pylint: disable=line-too-long

@dataclass
class _SensorIdentifier:
    """Sensor identifier used by all *Condition classes."""

    lsid: int  # Logical sensor ID

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
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
    rx_state: Optional[RadioReceptionState]  #: Radio reception state
    trans_battery_flag: int  #: Transmitter battery flag

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
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

    Data structure for `data_structure_type = 1`
    """

    temp: Optional[float]  #: Temperature [`TemperatureUnit`]
    hum: Optional[float]  #: Humidity [%]
    dew_point: Optional[float]  #: Dew point [`TemperatureUnit`]
    wet_bulb: Optional[float]  #: Wet bulb [`TemperatureUnit`]
    heat_index: Optional[float]  #: Heat index [`TemperatureUnit`]
    wind_chill: Optional[float]  #: Wind chill [`TemperatureUnit`]
    thw_index: Optional[float]  #: THW index [`TemperatureUnit`]
    thsw_index: Optional[float]  #: THSW index [`TemperatureUnit`]

    wind_speed_last: Optional[float]  #: Most recent wind speed [`WindSpeedUnit`]
    wind_speed_avg_last_1_min: Optional[float]  #: Average wind speed over last 1 min [`WindSpeedUnit`]
    wind_speed_avg_last_2_min: Optional[float]  #: Average wind speed over last 2 min [`WindSpeedUnit`]
    wind_speed_avg_last_10_min: Optional[float]  #: Average wind speed over last 10 min [`WindSpeedUnit`]
    wind_speed_hi_last_2_min: Optional[float]  #: Maximum wind speed over last 2 min [`WindSpeedUnit`]
    wind_speed_hi_last_10_min: Optional[float]  #: Maximum wind speed over last 10 min [`WindSpeedUnit`]

    wind_dir_last: Optional[float]  #: Wind direction [°]
    wind_dir_scalar_avg_last_1_min: Optional[float]  #: Average wind direction over last 1 min [°]
    wind_dir_scalar_avg_last_2_min: Optional[float]  #: Average wind direction over last 2 min [°]
    wind_dir_scalar_avg_last_10_min: Optional[float]  #: Average wind direction over last 10 min [°]
    wind_dir_at_hi_speed_last_2_min: Optional[float]  #: Gust wind direction over last 2 min [°]
    wind_dir_at_hi_speed_last_10_min: Optional[float]  #: Gust wind direction over last 10 min [°]

    rainfall_last_60_min: Optional[float]  #: Total rain for last 60 min [`RainUnit`]
    rainfall_last_24_hr: Optional[float]  #: Total rain for last 24 hours [`RainUnit`]
    rainfall_daily: Optional[float]  #: Total rain since local midnight [`RainUnit`]
    rainfall_monthly: Optional[float]  #: Total rain since first of month [`RainUnit`]
    rainfall_year: Optional[float]  #: Total rain since first of user-chosen month at local midnight [`RainUnit`]

    rain_rate_last: Optional[float]  #: Rain rate [`RainUnit`/hour]
    rain_rate_hi_last_1_min: Optional[float]  #: Highest rain rate over last 1 min [`RainUnit`/hour]
    rain_rate_hi_last_15_min: Optional[float]  #: Highest rain rate over last 15 min [`RainUnit`/hour]

    rain_storm_last: Optional[float]  #: Total rain since last 24 hour long break in rain [`RainUnit`]
    rain_storm_last_start_at: Optional[datetime]  #: Timestamp of last rain storm start
    rain_storm_last_end_at: Optional[datetime]  #: Timestamp of last rain storm start

    solar_rad: Optional[float]  #: Solar radiation [W/m²]
    uv_index: Optional[float]  #: UV index

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
        rain_size_inches = {
            1: 0.01,  # 0.01"
            2: 0.2 / 25.4,  # 0.2 mm
            3: 0.1 / 25.4,  # 0.1 mm
            4: 0.001,  # 0.001"
        }[json_data["rain_size"]]

        def counts_to_inch(counts: Optional[int]) -> Optional[float]:
            if counts is None:
                return None
            return counts * rain_size_inches

        def to_datetime(timestamp: Optional[int]) -> Optional[datetime]:
            if timestamp is None:
                return None
            return datetime.fromtimestamp(timestamp)

        return cls(  # type: ignore
            **asdict(_SensorIdentifier.from_dict(json_data)),
            **asdict(_WirelessSensorUnit.from_dict(json_data)),
            temp=convert_temperature(json_data["temp"]),
            hum=convert_temperature(json_data["hum"]),
            dew_point=convert_temperature(json_data["dew_point"]),
            wet_bulb=convert_temperature(json_data["wet_bulb"]),
            heat_index=convert_temperature(json_data["heat_index"]),
            wind_chill=convert_temperature(json_data["wind_chill"]),
            thw_index=convert_temperature(json_data["thw_index"]),
            thsw_index=convert_temperature(json_data["thsw_index"]),

            wind_speed_last=convert_wind_speed(json_data["wind_speed_last"]),
            wind_speed_avg_last_1_min=convert_wind_speed(json_data["wind_speed_avg_last_1_min"]),
            wind_speed_avg_last_2_min=convert_wind_speed(json_data["wind_speed_avg_last_2_min"]),
            wind_speed_avg_last_10_min=convert_wind_speed(json_data["wind_speed_avg_last_10_min"]),
            wind_speed_hi_last_2_min=convert_wind_speed(json_data["wind_speed_hi_last_2_min"]),
            wind_speed_hi_last_10_min=convert_wind_speed(json_data["wind_speed_hi_last_10_min"]),

            wind_dir_last=json_data["wind_dir_last"],
            wind_dir_scalar_avg_last_1_min=json_data["wind_dir_scalar_avg_last_1_min"],
            wind_dir_scalar_avg_last_2_min=json_data["wind_dir_scalar_avg_last_2_min"],
            wind_dir_scalar_avg_last_10_min=json_data["wind_dir_scalar_avg_last_10_min"],
            wind_dir_at_hi_speed_last_2_min=json_data["wind_dir_at_hi_speed_last_2_min"],
            wind_dir_at_hi_speed_last_10_min=json_data["wind_dir_at_hi_speed_last_10_min"],

            rainfall_last_60_min=convert_rain(counts_to_inch(json_data["rainfall_last_60_min"])),
            rainfall_last_24_hr=convert_rain(counts_to_inch(json_data["rainfall_last_24_hr"])),
            rainfall_daily=convert_rain(counts_to_inch(json_data["rainfall_daily"])),
            rainfall_monthly=convert_rain(counts_to_inch(json_data["rainfall_monthly"])),
            rainfall_year=convert_rain(counts_to_inch(json_data["rainfall_year"])),

            rain_rate_last=convert_rain(counts_to_inch(json_data["rain_rate_last"])),
            rain_rate_hi_last_1_min=convert_rain(counts_to_inch(json_data["rain_rate_hi"])),
            rain_rate_hi_last_15_min=convert_rain(counts_to_inch(json_data["rain_rate_hi_last_15_min"])),

            rain_storm_last=convert_rain(counts_to_inch(json_data["rain_storm_last"])),
            rain_storm_last_start_at=to_datetime(json_data["rain_storm_last_start_at"]),
            rain_storm_last_end_at=to_datetime(json_data["rain_storm_last_end_at"]),

            solar_rad=json_data["solar_rad"],
            uv_index=json_data["uv_index"],
        )


@dataclass
class MoistureTemperatureConditions(_SensorIdentifier, _WirelessSensorUnit):
    """
    Conditions of leaf & soil moisture/temperature station.

    Data structure for `data_structure_type = 2`
    """

    temp_1: Optional[float]  #: Temperature slot 1 [`TemperatureUnit`]
    temp_2: Optional[float]  #: Temperature slot 2 [`TemperatureUnit`]
    temp_3: Optional[float]  #: Temperature slot 3 [`TemperatureUnit`]
    temp_4: Optional[float]  #: Temperature slot 4 [`TemperatureUnit`]
    moist_soil_1: Optional[float]  #: Moisture soil slot 1 [cb]
    moist_soil_2: Optional[float]  #: Moisture soil slot 2 [cb]
    moist_soil_3: Optional[float]  #: Moisture soil slot 3 [cb]
    moist_soil_4: Optional[float]  #: Moisture soil slot 4 [cb]
    wet_leaf_1: Optional[float]  #: Leaf wetness slot 1
    wet_leaf_2: Optional[float]  #: Leaf wetness slot 2

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
        assert json_data["data_structure_type"] == 2
        return cls(  # type: ignore
            **asdict(_SensorIdentifier.from_dict(json_data)),
            **asdict(_WirelessSensorUnit.from_dict(json_data)),
            temp_1=convert_temperature(json_data["temp_1"]),
            temp_2=convert_temperature(json_data["temp_2"]),
            temp_3=convert_temperature(json_data["temp_3"]),
            temp_4=convert_temperature(json_data["temp_4"]),
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

    Data structure for `data_structure_type = 3`
    """

    bar_sea_level: Optional[float]  #: Most recent bar sensor reading with elevation adjustment [`PressureUnit`]
    bar_trend: Optional[float]  #: Current 3 hour bar trend [`PressureUnit`]
    bar_absolute: Optional[float]  #: Raw bar sensor reading [`PressureUnit`]

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
        assert json_data["data_structure_type"] == 3
        return cls(  # type: ignore
            **asdict(_SensorIdentifier.from_dict(json_data)),
            bar_absolute=convert_pressure(json_data["bar_absolute"]),
            bar_sea_level=convert_pressure(json_data["bar_sea_level"]),
            bar_trend=convert_pressure(json_data["bar_trend"]),
        )


@dataclass
class InsideConditions(_SensorIdentifier):
    """
    Inside conditions of WeatherLink Live station.

    Data structure for `data_structure_type = 4`
    """

    temp: Optional[float]  #: Inside temperature [`TemperatureUnit`]
    hum: Optional[float]  #: Inside humidity [%]
    dew_point: Optional[float]  #: Dew point [`TemperatureUnit`]
    heat_index: Optional[float]  #: Heat index [`TemperatureUnit`]

    @classmethod
    def from_dict(cls, json_data: Dict[str, Any]):
        assert json_data["data_structure_type"] == 4
        return cls(  # type: ignore
            **asdict(_SensorIdentifier.from_dict(json_data)),
            temp=convert_temperature(json_data["temp_in"]),
            hum=json_data["hum_in"],
            dew_point=convert_temperature(json_data["dew_point_in"]),
            heat_index=convert_temperature(json_data["heat_index_in"]),
        )


@dataclass
class Conditions:
    """
    Gathered conditions of all available sensors.

    Returned by `get_conditions` function.
    """

    timestamp: datetime  #: Timestamp
    inside: InsideConditions  #: Inside conditions of WeatherLink Live station
    barometric: BarometricConditions  #: Barometric conditions of WeatherLink Live station
    integrated_sensor_suites: List[MoistureTemperatureConditions]  #: Conditions of leaf & soil moisture/temperature station(s)
    moisture_temperature_stations: List[SensorSuiteConditions]  #: Conditions of integrated sensor suite(s), e.g. Vantage Vue
