"""
Main Uptime Kuma API Client

Combines REST and Socket.io functionality for comprehensive Uptime Kuma interaction.
"""

import asyncio
from typing import Optional, Dict, Any, List
from .rest_client import UptimeKumaRESTClient
from .socket_client import UptimeKumaSocketClient


class UptimeKumaClient:
    """
    Main client that combines REST and Socket.io APIs for Uptime Kuma.

    This client provides both synchronous REST operations and asynchronous
    real-time monitoring via Socket.io.
    """

    def __init__(self, base_url: str, username: Optional[str] = None, password: Optional[str] = None,
                 api_key: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the Uptime Kuma client.

        Args:
            base_url: Base URL of the Uptime Kuma instance (e.g., 'http://localhost:3001')
            username: Username for authentication (optional if using API key)
            password: Password for authentication (optional if using API key)
            api_key: API key for authentication (optional if using username/password)
            token: JWT token for authentication (optional, for token-based auth)
        """
        self.base_url = base_url.rstrip('/')
        self.rest_client = UptimeKumaRESTClient(base_url, username, password, api_key)
        self.socket_client = UptimeKumaSocketClient(base_url, username, password, token)

    async def connect(self) -> bool:
        """
        Connect to Uptime Kuma via Socket.io.

        Returns:
            True if connection successful, False otherwise
        """
        return await self.socket_client.connect()

    async def disconnect(self):
        """Disconnect from Socket.io."""
        await self.socket_client.disconnect()

    # REST API Methods
    def get_status_page(self, slug: str) -> Dict[str, Any]:
        """Get status page data."""
        return self.rest_client.get_status_page(slug)

    def get_status_page_heartbeat(self, slug: str) -> Dict[str, Any]:
        """Get status page heartbeat data."""
        return self.rest_client.get_status_page_heartbeat(slug)

    def push_monitor_status(self, push_token: str, status: str = "up",
                          msg: str = "OK", ping: Optional[float] = None) -> Dict[str, Any]:
        """Push status update for a monitor."""
        return self.rest_client.push_monitor_status(push_token, status, msg, ping)

    def get_metrics(self) -> str:
        """Get Prometheus metrics."""
        return self.rest_client.get_metrics()

    # Socket.io Methods
    async def login(self, username: str, password: str, token: Optional[str] = None) -> Dict[str, Any]:
        """Login via Socket.io."""
        return await self.socket_client.login(username, password, token)

    async def login_by_token(self, jwt_token: str) -> Dict[str, Any]:
        """Login using JWT token via Socket.io."""
        return await self.socket_client.login_by_token(jwt_token)

    async def add_monitor(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new monitor."""
        return await self.socket_client.add_monitor(monitor_data)

    async def edit_monitor(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Edit an existing monitor."""
        return await self.socket_client.edit_monitor(monitor_data)

    async def delete_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Delete a monitor."""
        return await self.socket_client.delete_monitor(monitor_id)

    async def pause_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Pause a monitor."""
        return await self.socket_client.pause_monitor(monitor_id)

    async def resume_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Resume a monitor."""
        return await self.socket_client.resume_monitor(monitor_id)

    async def get_monitor_beats(self, monitor_id: int, period: int = 24) -> Dict[str, Any]:
        """Get monitor heartbeat data."""
        return await self.socket_client.get_monitor_beats(monitor_id, period)

    async def add_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a notification."""
        return await self.socket_client.add_notification(notification_data)

    async def delete_notification(self, notification_id: int) -> Dict[str, Any]:
        """Delete a notification."""
        return await self.socket_client.delete_notification(notification_id)

    # Event handlers
    def on_heartbeat(self, callback):
        """Register callback for heartbeat events."""
        self.socket_client.on_heartbeat(callback)

    def on_monitor_list_update(self, callback):
        """Register callback for monitor list updates."""
        self.socket_client.on_monitor_list_update(callback)

    def on_uptime_update(self, callback):
        """Register callback for uptime updates."""
        self.socket_client.on_uptime_update(callback)
