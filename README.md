# WeatherLink Live Local Python API

Python library to read weather data from a [Davis® WeatherLink Live station](https://www.davisinstruments.com/weatherlinklive/) + connected sensors (e.g. [Vantage Vue](https://www.davisinstruments.com/vantage-vue/)). Features:

- discover WeatherLink Live stations in the local network
- read sensor values (called conditions) using the **local** API - no internet connection required

Although the WeatherLink Live stations are tighly coupled with the web service [weatherlink.com](https://www.weatherlink.com/), it can be used in offline situations aswell. The well designed HTTP interface makes it easy to read the current weather data via the local network - perfect for IoT / SmartHome applications.
In fact, I couldn't find any other commercial weather station with an open ethernet-based protocol (please correct me if I'm wrong).

To set up the WeatherLink Live stations, you need the Davis WeatherLink app ([Android](https://play.google.com/store/apps/details?id=com.davisinstruments.weatherlink), [iOS](https://apps.apple.com/us/app/weatherlink/id1304504954)) and a weatherlink.com account. Further sensors can be connected to the station.
Afterwards, the weather data is accessible via weatherlink.com (if online) and the local API.

## Documentation

Python library: https://weatherlink-live-local-python.rtfd.io/

API specification: https://weatherlink.github.io/weatherlink-live-local-api/

## Install

```
pip install weatherlink_live_local
```

## Example

```python
import weatherlink_live_local as wlll

devices = wlll.discover()
print(devices)

# select first device, get IP address
ip_first_device = devices[0].ip_addresses[0]

# specify units
wlll.set_units(
    temperature=wlll.units.TemperatureUnit.CELSIUS,
    pressure=wlll.units.PressureUnit.HECTOPASCAL,
    rain=wlll.units.RainUnit.MILLIMETER,
    wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND,
)

# poll sensor data / conditions
while True:
    conditions = wlll.get_conditions(ip_first_device)
    print(f"Inside temperature:  {conditions.inside.temp:.2f} °C")
    print(f"Outside temperature: {conditions.integrated_sensor_suites[0].temp:.2f} °C")
    time.sleep(10)
```
