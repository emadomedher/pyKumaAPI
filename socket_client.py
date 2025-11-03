"""
Uptime Kuma Socket.io API Client

Handles real-time communication with Uptime Kuma via Socket.io.
"""

import asyncio
import json
from typing import Optional, Dict, Any, Callable, List
import socketio
from urllib.parse import urljoin


class UptimeKumaSocketClient:
    """
    Socket.io client for Uptime Kuma real-time API.

    Handles authentication and real-time events.
    """

    def __init__(self, base_url: str, username: Optional[str] = None,
                 password: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize the Socket.io client.

        Args:
            base_url: Base URL of the Uptime Kuma instance
            username: Username for authentication
            password: Password for authentication
            token: JWT token for authentication (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = token

        # Socket.io client
        self.sio = socketio.AsyncClient()
        self.connected = False
        self.authenticated = False

        # Event callbacks
        self._heartbeat_callbacks: List[Callable] = []
        self._monitor_list_callbacks: List[Callable] = []
        self._uptime_callbacks: List[Callable] = []

        # Set up event handlers
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Set up Socket.io event handlers."""

        @self.sio.event
        async def connect():
            self.connected = True
            print("Connected to Uptime Kuma")

        @self.sio.event
        async def disconnect():
            self.connected = False
            self.authenticated = False
            print("Disconnected from Uptime Kuma")

        @self.sio.event
        async def loginRequired():
            print("Login required")

        @self.sio.event
        async def heartbeat(data):
            """Handle heartbeat events."""
            for callback in self._heartbeat_callbacks:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in heartbeat callback: {e}")

        @self.sio.event
        async def monitorList(data):
            """Handle monitor list updates."""
            for callback in self._monitor_list_callbacks:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in monitor list callback: {e}")

        @self.sio.event
        async def uptime(data):
            """Handle uptime updates."""
            for callback in self._uptime_callbacks:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in uptime callback: {e}")

        @self.sio.event
        async def info(data):
            """Handle server info."""
            print(f"Server info: {data}")

    async def connect(self) -> bool:
        """
        Connect to Uptime Kuma via Socket.io.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            socket_url = urljoin(self.base_url, '/socket.io/')
            await self.sio.connect(socket_url)
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    async def disconnect(self):
        """Disconnect from Socket.io."""
        if self.connected:
            await self.sio.disconnect()

    async def _emit_with_callback(self, event: str, data: Any = None) -> Dict[str, Any]:
        """Emit event and wait for callback response."""
        future = asyncio.Future()

        def callback(response):
            if not future.done():
                future.set_result(response)

        if data is not None:
            await self.sio.emit(event, data, callback=callback)
        else:
            await self.sio.emit(event, callback=callback)

        try:
            return await asyncio.wait_for(future, timeout=30.0)
        except asyncio.TimeoutError:
            return {"ok": False, "msg": "Request timeout"}

    async def login(self, username: str, password: str, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Login via Socket.io.

        Args:
            username: Username
            password: Password
            token: 2FA token (optional)

        Returns:
            Login response
        """
        data = {
            "username": username,
            "password": password
        }
        if token:
            data["token"] = token

        response = await self._emit_with_callback("login", data)
        if response.get("ok"):
            self.authenticated = True
        return response

    async def login_by_token(self, jwt_token: str) -> Dict[str, Any]:
        """
        Login using JWT token.

        Args:
            jwt_token: JWT token

        Returns:
            Login response
        """
        response = await self._emit_with_callback("loginByToken", jwt_token)
        if response.get("ok"):
            self.authenticated = True
        return response

    async def logout(self) -> Dict[str, Any]:
        """Logout."""
        response = await self._emit_with_callback("logout")
        if response.get("ok"):
            self.authenticated = False
        return response

    # Monitor Management
    async def add_monitor(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new monitor."""
        return await self._emit_with_callback("add", monitor_data)

    async def edit_monitor(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Edit an existing monitor."""
        return await self._emit_with_callback("editMonitor", monitor_data)

    async def delete_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Delete a monitor."""
        return await self._emit_with_callback("deleteMonitor", monitor_id)

    async def pause_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Pause a monitor."""
        return await self._emit_with_callback("pauseMonitor", monitor_id)

    async def resume_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Resume a monitor."""
        return await self._emit_with_callback("resumeMonitor", monitor_id)

    async def get_monitor(self, monitor_id: int) -> Dict[str, Any]:
        """Get monitor details."""
        return await self._emit_with_callback("getMonitor", monitor_id)

    async def get_monitor_beats(self, monitor_id: int, period: int = 24) -> Dict[str, Any]:
        """Get monitor heartbeat data."""
        data = {"monitorID": monitor_id, "period": period}
        return await self._emit_with_callback("getMonitorBeats", data)

    async def get_monitor_chart_data(self, monitor_id: int, period: int = 24) -> Dict[str, Any]:
        """Get monitor chart data."""
        data = {"monitorID": monitor_id, "period": period}
        return await self._emit_with_callback("getMonitorChartData", data)

    # Notification Management
    async def add_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a notification."""
        return await self._emit_with_callback("addNotification", notification_data)

    async def delete_notification(self, notification_id: int) -> Dict[str, Any]:
        """Delete a notification."""
        return await self._emit_with_callback("deleteNotification", notification_id)

    async def test_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test a notification."""
        return await self._emit_with_callback("testNotification", notification_data)

    # Status Page Management
    async def add_status_page(self, title: str, slug: str) -> Dict[str, Any]:
        """Add a status page."""
        data = {"title": title, "slug": slug}
        return await self._emit_with_callback("addStatusPage", data)

    async def save_status_page(self, slug: str, config: Dict[str, Any],
                             public_group_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Save status page configuration."""
        data = {
            "slug": slug,
            "config": config,
            "publicGroupList": public_group_list
        }
        return await self._emit_with_callback("saveStatusPage", data)

    async def delete_status_page(self, slug: str) -> Dict[str, Any]:
        """Delete a status page."""
        return await self._emit_with_callback("deleteStatusPage", slug)

    # Settings
    async def get_settings(self) -> Dict[str, Any]:
        """Get server settings."""
        return await self._emit_with_callback("getSettings")

    async def set_settings(self, settings: Dict[str, Any], current_password: str = "") -> Dict[str, Any]:
        """Set server settings."""
        data = {"settings": settings, "currentPassword": current_password}
        return await self._emit_with_callback("setSettings", data)

    async def change_password(self, current_password: str, new_password: str) -> Dict[str, Any]:
        """Change password."""
        data = {
            "passwords": {
                "currentPassword": current_password,
                "newPassword": new_password
            }
        }
        return await self._emit_with_callback("changePassword", data)

    # Event callback registration
    def on_heartbeat(self, callback: Callable):
        """Register callback for heartbeat events."""
        self._heartbeat_callbacks.append(callback)

    def on_monitor_list_update(self, callback: Callable):
        """Register callback for monitor list updates."""
        self._monitor_list_callbacks.append(callback)

    def on_uptime_update(self, callback: Callable):
        """Register callback for uptime updates."""
        self._uptime_callbacks.append(callback)
