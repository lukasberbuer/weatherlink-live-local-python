"""Zeroconf-based discovery of WeatherLink Live services/devices in the local network(s)."""

import logging
import time
from typing import List, NamedTuple, Set

import zeroconf

logger = logging.getLogger(__name__)


class ServiceInfo(NamedTuple):
    """WeatherLink Live service information."""

    name: str  #: Unique name of service
    ip_addresses: List[str]  #: IP address of device, usually only one
    port: int  #: Port number, usually 80


class Discovery(zeroconf.ServiceListener):
    """
    Discovery for all WeatherLink Live services on local network(s).
    """

    TYPE = "_weatherlinklive._tcp.local."

    def __init__(self):
        self.services: Set[str] = set()

    # pylint: disable=unused-argument
    def add_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Found WeatherLink Live service '{name}'")
        self.services.add(name)

    def remove_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None:
        pass

    def update_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None:
        pass

    @classmethod
    def find(cls, timeout: float) -> List[ServiceInfo]:
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
