import logging
import time

import weatherlink_live_local as wlll

logging.basicConfig(level=logging.INFO)


def main():
    devices = wlll.discover()
    print(devices)

    # select first device, get IP address
    ip_first_device = devices[0].ip_addresses[0]

    # specify units
    units = wlll.units.Units(
        temperature=wlll.units.TemperatureUnit.CELSIUS,
        pressure=wlll.units.PressureUnit.HECTOPASCAL,
        rain=wlll.units.RainUnit.MILLIMETER,
        wind_speed=wlll.units.WindSpeedUnit.METER_PER_SECOND,
    )

    # poll sensor data / conditions
    while True:
        conditions = wlll.get_conditions(ip_first_device, units=units)
        print(f"Inside temperature:  {conditions.inside.temp:.2f} °C")
        print(f"Outside temperature: {conditions.integrated_sensor_suites[0].temp:.2f} °C")
        time.sleep(10)


if __name__ == "__main__":
    main()
