import re
from datetime import datetime, timezone

from httpretty import HTTPretty, httprettified

import weatherlink_live_local as wlll

RESPONSE_COMMENTS = """
{
    "data":
    {
        "did":"001D0A700002",
        "ts":1531754005,
        "conditions":[
            {
                "lsid":48308,                                  // logical sensor ID **(no unit)**
                "data_structure_type":1,                       // data structure type **(no unit)**
                "txid":1,                                      // transmitter ID **(no unit)**
                "temp":62.7,                                   // most recent valid temperature **(°F)**
                "hum":1.1,                                     // most recent valid humidity **(%RH)**
                "dew_point":-0.3,                              // **(°F)**
                "wet_bulb":null,                               // **(°F)**
                "heat_index":5.5,                              // **(°F)**
                "wind_chill":6.0,                              // **(°F)**
                "thw_index":5.5,                               // **(°F)**
                "thsw_index":5.5,                              // **(°F)**
                "wind_speed_last":2,                           // most recent valid wind speed **(mph)**
                "wind_dir_last":null,                          // most recent valid wind direction **(°degree)**
                "wind_speed_avg_last_1_min":4,                 // average wind speed over last 1 min **(mph)**
                "wind_dir_scalar_avg_last_1_min":15,           // scalar average wind direction over last 1 min **(°degree)**
                "wind_speed_avg_last_2_min":42606,             // average wind speed over last 2 min **(mph)**
                "wind_dir_scalar_avg_last_2_min":170.7,        // scalar average wind direction over last 2 min **(°degree)**
                "wind_speed_hi_last_2_min":8,                  // maximum wind speed over last 2 min **(mph)**
                "wind_dir_at_hi_speed_last_2_min":0.0,         // gust wind direction over last 2 min **(°degree)**
                "wind_speed_avg_last_10_min":42606,            // average wind speed over last 10 min **(mph)**
                "wind_dir_scalar_avg_last_10_min":4822.5,      // scalar average wind direction over last 10 min **(°degree)**
                "wind_speed_hi_last_10_min":8,                 // maximum wind speed over last 10 min **(mph)**
                "wind_dir_at_hi_speed_last_10_min":0.0,        // gust wind direction over last 10 min **(°degree)**
                "rain_size":2,                                 // rain collector type/size **(0: Reserved, 1: 0.01", 2: 0.2 mm, 3:  0.1 mm, 4: 0.001")**
                "rain_rate_last":0,                            // most recent valid rain rate **(counts/hour)**
                "rain_rate_hi":null,                           // highest rain rate over last 1 min **(counts/hour)**
                "rainfall_last_15_min":null,                   // total rain count over last 15 min **(counts)**
                "rain_rate_hi_last_15_min":0,                  // highest rain rate over last 15 min **(counts/hour)**
                "rainfall_last_60_min":null,                   // total rain count for last 60 min **(counts)**
                "rainfall_last_24_hr":null,                    // total rain count for last 24 hours **(counts)**
                "rain_storm":null,                             // total rain count since last 24 hour long break in rain **(counts)**
                "rain_storm_start_at":null,                    // UNIX timestamp of current rain storm start **(seconds)**
                "solar_rad":747,                               // most recent solar radiation **(W/m²)**
                "uv_index":5.5,                                // most recent UV index **(Index)**
                "rx_state":2,                                  // configured radio receiver state **(no unit)**
                "trans_battery_flag":0,                        // transmitter battery status flag **(no unit)**
                "rainfall_daily":63,                           // total rain count since local midnight **(counts)**
                "rainfall_monthly":63,                         // total rain count since first of month at local midnight **(counts)**
                "rainfall_year":63,                            // total rain count since first of user-chosen month at local midnight **(counts)**
                "rain_storm_last":null,                        // total rain count since last 24 hour long break in rain **(counts)**
                "rain_storm_last_start_at":null,               // UNIX timestamp of last rain storm start **(sec)**
                "rain_storm_last_end_at":null                  // UNIX timestamp of last rain storm end **(sec)**
            },
            {
                "lsid":3187671188,
                "data_structure_type":2,
                "txid":3,
                "temp_1":null,                                 // most recent valid soil temp slot 1 **(°F)**
                "temp_2":null,                                 // most recent valid soil temp slot 2 **(°F)**
                "temp_3":null,                                 // most recent valid soil temp slot 3 **(°F)**
                "temp_4":null,                                 // most recent valid soil temp slot 4 **(°F)**
                "moist_soil_1":null,                           // most recent valid soil moisture slot 1 **(|cb|)**
                "moist_soil_2":null,                           // most recent valid soil moisture slot 2 **(|cb|)**
                "moist_soil_3":null,                           // most recent valid soil moisture slot 3 **(|cb|)**
                "moist_soil_4":null,                           // most recent valid soil moisture slot 4 **(|cb|)**
                "wet_leaf_1":null,                             // most recent valid leaf wetness slot 1 **(no unit)**
                "wet_leaf_2":null,                             // most recent valid leaf wetness slot 2 **(no unit)**
                "rx_state":null,                               // configured radio receiver state **(no unit)**
                "trans_battery_flag":null                      // transmitter battery status flag **(no unit)**
            },
            {
                "lsid":48307,
                "data_structure_type":4,
                "temp_in":78.0,                                // most recent valid inside temp **(°F)**
                "hum_in":41.1,                                 // most recent valid inside humidity **(%RH)**
                "dew_point_in":7.8,                            // **(°F)**
                "heat_index_in":8.4                            // **(°F)**
            },
            {
                "lsid":48306,
                "data_structure_type":3,
                "bar_sea_level":30.008,                        // most recent bar sensor reading with elevation adjustment **(inches)**
                "bar_trend":null,                              // current 3 hour bar trend **(inches)**
                "bar_absolute":30.008                          // raw bar sensor reading **(inches)**
            }
        ]
    },
    "error":null
}
"""

RESPONSE = re.sub(r"\s+//.*$", "", RESPONSE_COMMENTS, flags=re.MULTILINE)
RAIN_SIZE_INCH = 0.2 / 25.4


def _counts_to_inch(counts: int) -> float:
    return counts * RAIN_SIZE_INCH


def test_parse_response():  # noqa: PLR0915
    units = wlll.units.Units()
    conditions = wlll.parse_response(RESPONSE, units)

    assert conditions.timestamp == datetime.fromtimestamp(1531754005, timezone.utc)

    inside = conditions.inside
    assert isinstance(inside, wlll.conditions.InsideConditions)
    assert inside.lsid == 48307
    assert inside.temp == 78
    assert inside.hum == 41.1
    assert inside.dew_point == 7.8
    assert inside.heat_index == 8.4

    barometric = conditions.barometric
    assert isinstance(barometric, wlll.conditions.BarometricConditions)
    assert barometric.lsid == 48306
    assert barometric.bar_absolute == 30.008
    assert barometric.bar_sea_level == 30.008
    assert barometric.bar_trend is None

    assert len(conditions.moisture_temperature_stations) == 1
    mt0 = conditions.moisture_temperature_stations[0]
    assert isinstance(mt0, wlll.conditions.MoistureTemperatureConditions)
    assert mt0.txid == 3
    assert mt0.rx_state is None
    assert mt0.trans_battery_flag is None
    assert mt0.temp_1 is None
    assert mt0.temp_2 is None
    assert mt0.temp_3 is None
    assert mt0.temp_4 is None
    assert mt0.moist_soil_1 is None
    assert mt0.moist_soil_2 is None
    assert mt0.moist_soil_3 is None
    assert mt0.moist_soil_4 is None
    assert mt0.wet_leaf_1 is None
    assert mt0.wet_leaf_2 is None

    assert len(conditions.integrated_sensor_suites) == 1
    iss0 = conditions.integrated_sensor_suites[0]
    assert isinstance(iss0, wlll.conditions.SensorSuiteConditions)
    assert iss0.lsid == 48308
    assert iss0.txid == 1
    assert iss0.rx_state == wlll.conditions.RadioReceptionState.SCANNING
    assert iss0.trans_battery_flag == 0
    assert iss0.temp == 62.7
    assert iss0.hum == 1.1
    assert iss0.dew_point == -0.3
    assert iss0.wet_bulb is None
    assert iss0.heat_index == 5.5
    assert iss0.wind_chill == 6.0
    assert iss0.thw_index == 5.5
    assert iss0.thsw_index == 5.5
    assert iss0.wind_speed_last == 2
    assert iss0.wind_speed_avg_last_1_min == 4
    assert iss0.wind_speed_avg_last_2_min == 42606
    assert iss0.wind_speed_avg_last_10_min == 42606
    assert iss0.wind_speed_hi_last_2_min == 8
    assert iss0.wind_speed_hi_last_10_min == 8
    assert iss0.wind_dir_last is None
    assert iss0.wind_dir_scalar_avg_last_1_min == 15
    assert iss0.wind_dir_scalar_avg_last_2_min == 170.7
    assert iss0.wind_dir_scalar_avg_last_10_min == 4822.5
    assert iss0.wind_dir_at_hi_speed_last_2_min == 0.0
    assert iss0.wind_dir_at_hi_speed_last_10_min == 0.0
    assert iss0.rainfall_last_60_min is None
    assert iss0.rainfall_last_24_hr is None
    assert iss0.rainfall_daily == _counts_to_inch(63)
    assert iss0.rainfall_monthly == _counts_to_inch(63)
    assert iss0.rainfall_year == _counts_to_inch(63)
    assert iss0.rain_rate_last == 0
    assert iss0.rain_rate_hi_last_1_min is None
    assert iss0.rain_rate_hi_last_15_min == 0
    assert iss0.rain_storm_last is None
    assert iss0.rain_storm_last_start_at is None
    assert iss0.rain_storm_last_end_at is None
    assert iss0.solar_rad == 747
    assert iss0.uv_index == 5.5


@httprettified
def test_get_conditions():
    HTTPretty.register_uri(
        HTTPretty.GET,
        "http://127.0.0.1/v1/current_conditions",
        body=RESPONSE,
    )

    units = wlll.units.Units(
        temperature=wlll.units.TemperatureUnit.CELSIUS,
        pressure=wlll.units.PressureUnit.HECTOPASCAL,
        rain=wlll.units.RainUnit.MILLIMETER,
        wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND,
    )
    conditions = wlll.get_conditions("127.0.0.1", units)
    assert conditions == wlll.parse_response(RESPONSE, units)
