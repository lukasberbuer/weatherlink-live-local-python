"""WeatherLink Live Local Python API."""

from __future__ import annotations

import json
import urllib.request

from weatherlink_live_local import conditions, discovery, units


def discover(timeout: int = 1) -> list[discovery.ServiceInfo]:
    """
    Discover all WeatherLink Live services on local network(s).

    Args:
        timeout: Timeout in seconds

    Returns:
        List of found services
    """
    return discovery.Discovery.find(timeout=timeout)


def parse_response(json_str: str, units: units.Units) -> conditions.Conditions:
    """
    Parse JSON response from WeatherLink Live API.

    Args:
        json_str: Raw JSON response as str
        units: Units of the conditions

    Returns:
        Conditions of all available sensors
    """
    json_dict = json.loads(json_str)
    return conditions.Conditions.from_dict(json_dict["data"], units)


def get_conditions(
    ip: str,
    units: units.Units,
    port: int = 80,
    timeout: int = 1,
) -> conditions.Conditions:
    """
    Read conditions from WeatherLink Live device + all connected sensors.

    Args:
        ip: IP address of WeatherLink Live device.
            Use `discover` function to find devices with their IP address in the local network.
        units: Units of the conditions
        port: Port number of HTTP interface, should be 80
        timeout: Maximum time to listen for WeatherLink Live services

    Returns:
        Conditions of all available sensors
    """
    url = f"http://{ip}:{port}/v1/current_conditions"
    with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310
        if resp.status != 200:
            raise RuntimeError(f"HTTP response code {resp.status}")

        json_str = resp.read().decode("utf-8")
        return parse_response(json_str, units)
