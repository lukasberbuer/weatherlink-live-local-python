"""Zeroconf-based discovery of WeatherLink Live services/devices in the local network(s)."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

import zeroconf
import zeroconf.asyncio

ZEROCONF_SERVICE = "_weatherlinklive._tcp.local."


@dataclass
class ServiceInfo:
    """WeatherLink Live service information."""

    name: str  #: Unique name of service
    ip_addresses: list[str]  #: IP address of device, usually only one
    port: int | None  #: Port number, usually 80


def discover(timeout: float = 1.0) -> list[ServiceInfo]:
    """
    Discover all WeatherLink Live services on local network(s).

    Args:
        timeout: Timeout in seconds

    Returns:
        List of discovered services
    """
    names = set()

    def handler(name: str, state_change: zeroconf.ServiceStateChange, **kwargs):  # noqa: ARG001
        if state_change == zeroconf.ServiceStateChange.Added:
            names.add(name)

    with zeroconf.Zeroconf() as zc:
        with zeroconf.ServiceBrowser(zc, ZEROCONF_SERVICE, handlers=[handler]):
            time.sleep(timeout)

        return [
            ServiceInfo(name=info.name, ip_addresses=info.parsed_addresses(), port=info.port)
            for info in [zc.get_service_info(ZEROCONF_SERVICE, name) for name in names]
            if info is not None
        ]


async def discover_async(timeout: float = 1.0) -> list[ServiceInfo]:
    """
    Asynchronously discover all WeatherLink Live services on local network(s).

    Args:
        timeout: Timeout in seconds

    Returns:
        List of found services
    """
    names = set()

    def handler(name: str, state_change: zeroconf.ServiceStateChange, **kwargs):  # noqa: ARG001
        if state_change == zeroconf.ServiceStateChange.Added:
            names.add(name)

    async with zeroconf.asyncio.AsyncZeroconf() as zc:
        async with zeroconf.asyncio.AsyncServiceBrowser(
            zc.zeroconf, ZEROCONF_SERVICE, handlers=[handler]
        ):
            await asyncio.sleep(timeout)

        return [
            ServiceInfo(name=info.name, ip_addresses=info.parsed_addresses(), port=info.port)
            for info in [await zc.async_get_service_info(ZEROCONF_SERVICE, name) for name in names]
            if info is not None
        ]
