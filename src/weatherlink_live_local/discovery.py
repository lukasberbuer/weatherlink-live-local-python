"""Zeroconf-based discovery of WeatherLink Live services/devices in the local network(s)."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import zeroconf

logger = logging.getLogger(__name__)


@dataclass
class ServiceInfo:
    """WeatherLink Live service information."""

    name: str  #: Unique name of service
    ip_addresses: list[str]  #: IP address of device, usually only one
    port: int  #: Port number, usually 80


class Discovery(zeroconf.ServiceListener):
    """
    Discovery for all WeatherLink Live services on local network(s).
    """

    TYPE = "_weatherlinklive._tcp.local."

    def __init__(self):
        self.services: set[str] = set()

    # pylint: disable=unused-argument
    def add_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None:  # noqa: ARG002
        logger.info("Found WeatherLink Live service '%s'", name)
        self.services.add(name)

    def remove_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None: ...

    def update_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None: ...

    @classmethod
    def find(cls, timeout: float) -> list[ServiceInfo]:
        zc = zeroconf.Zeroconf()
        listener = cls()
        browser = zeroconf.ServiceBrowser(zc, cls.TYPE, listener=listener)

        time.sleep(timeout)  # wait for responses

        def get_service_infos():
            for name in sorted(listener.services):
                zc_service_info = zc.get_service_info(cls.TYPE, name)
                yield ServiceInfo(
                    name=zc_service_info.name,
                    ip_addresses=zc_service_info.parsed_addresses(),
                    port=zc_service_info.port,
                )

        service_infos = list(get_service_infos())
        browser.cancel()
        zc.close()
        return service_infos
