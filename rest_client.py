"""
Uptime Kuma REST API Client

Handles REST API interactions with Uptime Kuma.
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
import base64


class UptimeKumaRESTClient:
    """
    REST API client for Uptime Kuma.

    Handles authentication and REST endpoint interactions.
    """

    def __init__(self, base_url: str, username: Optional[str] = None,
                 password: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the REST client.

        Args:
            base_url: Base URL of the Uptime Kuma instance
            username: Username for basic auth (optional if using API key)
            password: Password for basic auth (optional if using API key)
            api_key: API key for authentication (optional if using username/password)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session = requests.Session()

        # Set up authentication
        if api_key:
            # API key authentication for metrics endpoint
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
        elif username and password:
            # Basic auth for metrics endpoint
            auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
            self.session.headers.update({
                'Authorization': f'Basic {auth_string}'
            })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request and handle common response processing."""
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()

        # Handle different response types
        if response.headers.get('content-type', '').startswith('application/json'):
            return response.json()
        else:
            return {'content': response.text, 'status_code': response.status_code}

    def push_monitor_status(self, push_token: str, status: str = "up",
                          msg: str = "OK", ping: Optional[float] = None) -> Dict[str, Any]:
        """
        Push status update for a monitor.

        Args:
            push_token: The push token for the monitor
            status: Status ("up" or "down")
            msg: Status message
            ping: Response time in milliseconds (optional)

        Returns:
            API response
        """
        params = {'status': status, 'msg': msg}
        if ping is not None:
            params['ping'] = ping

        return self._make_request('GET', f'api/push/{push_token}', params=params)

    def get_status_page(self, slug: str) -> Dict[str, Any]:
        """
        Get status page data.

        Args:
            slug: Status page slug

        Returns:
            Status page data
        """
        return self._make_request('GET', f'api/status-page/{slug}')

    def get_status_page_heartbeat(self, slug: str) -> Dict[str, Any]:
        """
        Get status page heartbeat data.

        Args:
            slug: Status page slug

        Returns:
            Heartbeat data
        """
        return self._make_request('GET', f'api/status-page/heartbeat/{slug}')

    def get_metrics(self) -> str:
        """
        Get Prometheus metrics.

        Returns:
            Metrics in Prometheus format
        """
        response = self._make_request('GET', 'metrics')
        if isinstance(response, dict) and 'content' in response:
            return response['content']
        return str(response)

    def get_entry_page(self) -> Dict[str, Any]:
        """
        Get entry page information.

        Returns:
            Entry page data
        """
        return self._make_request('GET', 'api/entry-page')

    def close(self):
        """Close the session."""
        self.session.close()
