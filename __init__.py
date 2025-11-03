"""
Uptime Kuma API Client

A Python client for interacting with Uptime Kuma's REST and Socket.io APIs.
"""

from .client import UptimeKumaClient
from .rest_client import UptimeKumaRESTClient
from .socket_client import UptimeKumaSocketClient

__version__ = "0.1.0"
__all__ = ["UptimeKumaClient", "UptimeKumaRESTClient", "UptimeKumaSocketClient"]
