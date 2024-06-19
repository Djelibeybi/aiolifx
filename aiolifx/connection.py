import asyncio
import logging

from .aiolifx import UDP_BROADCAST_PORT, Light, LifxDiscovery, DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)

class LIFXConnection:
    """Manage a connection to a LIFX device."""

    def __init__(self, host, mac, timeout: int = DEFAULT_TIMEOUT):
        """Init the connection."""
        self.host = host
        self.mac = mac
        self.device = None
        # self.transport = None
        self._timeout = timeout
        self._tasks = set()

    def register(self, device: Light):
        self.device = device

    def unregister(self, device: Light):
        self.async_stop()

    async def async_setup(self):
        """Ensure we are connected."""
        loop = asyncio.get_running_loop()
        discover_device = LifxDiscovery(loop, self, broadcast_ip=self.host)
        discovery = discover_device.start()

        try:
            await asyncio.wait_for(discovery, self._timeout)
        except TimeoutError:
            _LOGGER.debug("Timeout waiting for device to be discovered.")

        # self.transport, self.device = await loop.create_datagram_endpoint(
        #     lambda: Light(loop, self.mac, self.host),
        #     remote_addr=(self.host, UDP_BROADCAST_PORT),
        # )

    def async_stop(self):
        """Close the transport."""
        assert self.device is not None
        self.device.cleanup()

        # assert self.transport is not None
        # self.transport.close()
