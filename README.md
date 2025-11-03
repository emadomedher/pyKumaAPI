# pyKumaAPI

[![PyPI version](https://badge.fury.io/py/pyKumaAPI.svg)](https://badge.fury.io/py/pyKumaAPI)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyKumaAPI.svg)](https://pypi.org/project/pyKumaAPI/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python client for Uptime Kuma's REST and Socket.io APIs. This library provides both synchronous REST operations and asynchronous real-time monitoring capabilities.

## ⚠️ Important Notice

Uptime Kuma's API is primarily designed for the application's own use and is not officially supported for third-party integrations. Breaking changes may occur between versions without prior notice. Use at your own risk.

## Features

- 🔄 **Dual API Support**: Both REST endpoints and real-time Socket.io communication
- ⚡ **Asynchronous Operations**: Full async support for real-time events
- 📊 **Monitor Management**: Create, edit, delete, pause/resume monitors
- 🔔 **Real-time Events**: Callbacks for heartbeats, monitor updates, uptime changes
- 🔐 **Multiple Authentication**: Username/password, API key, and JWT token support
- 📈 **Status Page Integration**: Get status page data and heartbeat information
- 🛠️ **Notification Management**: Configure and test notifications
- ⚙️ **Settings Management**: Access and modify server settings

## Installation

```bash
pip install pyKumaAPI
```

Or install from source:

```bash
git clone https://github.com/emadomedher/pyKumaAPI.git
cd pyKumaAPI
pip install -r requirements.txt
pip install .
```

## Quick Start

### Basic Usage

```python
from uptime_kuma_api import UptimeKumaClient
import asyncio

async def main():
    # Initialize client
    client = UptimeKumaClient(
        base_url="http://localhost:3001",
        username="your_username",
        password="your_password"
    )

    try:
        # Connect via Socket.io
        connected = await client.connect()
        if not connected:
            print("Failed to connect")
            return

        # Login
        login_result = await client.login("your_username", "your_password")
        if not login_result.get("ok"):
            print(f"Login failed: {login_result.get('msg')}")
            return

        print("Successfully connected to Uptime Kuma!")

        # Get monitors
        monitors = await client.get_monitor_list()
        print(f"Monitors: {monitors}")

        # Create a new monitor
        monitor_data = {
            "name": "My Website",
            "type": "http",
            "url": "https://example.com",
            "interval": 60
        }
        result = await client.add_monitor(monitor_data)
        print(f"Created monitor: {result}")

    finally:
        await client.disconnect()

asyncio.run(main())
```

### REST API Only

```python
from uptime_kuma_api import UptimeKumaRESTClient

# Initialize REST client
client = UptimeKumaRESTClient(
    base_url="http://localhost:3001",
    username="your_username",
    password="your_password"
)

try:
    # Push monitor status
    result = client.push_monitor_status(
        push_token="your_push_token",
        status="up",
        msg="Service is running",
        ping=150.5
    )
    print(f"Push result: {result}")

    # Get status page
    status_page = client.get_status_page("your-status-page-slug")
    print(f"Status page: {status_page}")

finally:
    client.close()
```

### Real-time Event Handling

```python
from uptime_kuma_api import UptimeKumaClient
import asyncio

async def on_heartbeat(data):
    """Handle heartbeat events."""
    print(f"Heartbeat: {data}")

async def on_monitor_update(data):
    """Handle monitor list updates."""
    print(f"Monitor update: {data}")

async def main():
    client = UptimeKumaClient(
        base_url="http://localhost:3001",
        username="your_username",
        password="your_password"
    )

    # Register event handlers
    client.on_heartbeat(on_heartbeat)
    client.on_monitor_list_update(on_monitor_update)

    await client.connect()
    await client.login("username", "password")

    # Keep the connection alive
    await asyncio.sleep(300)  # Monitor for 5 minutes

    await client.disconnect()

asyncio.run(main())
```

## API Reference

### UptimeKumaClient

The main client that combines both REST and Socket.io functionality.

#### Initialization

```python
client = UptimeKumaClient(
    base_url="http://localhost:3001",  # Uptime Kuma instance URL
    username="your_username",          # Optional: username for auth
    password="your_password",          # Optional: password for auth
    api_key="your_api_key",            # Optional: API key for auth
    token="jwt_token"                  # Optional: JWT token
)
```

#### Connection Methods

- `await connect() -> bool`: Connect to Uptime Kuma via Socket.io
- `await disconnect()`: Disconnect from Socket.io

#### Authentication Methods

- `await login(username, password, token=None)`: Login via Socket.io
- `await login_by_token(jwt_token)`: Login using JWT token

#### Monitor Management

- `await add_monitor(monitor_data)`: Create a new monitor
- `await edit_monitor(monitor_data)`: Update an existing monitor
- `await delete_monitor(monitor_id)`: Delete a monitor
- `await pause_monitor(monitor_id)`: Pause a monitor
- `await resume_monitor(monitor_id)`: Resume a monitor
- `await get_monitor(monitor_id)`: Get monitor details
- `await get_monitor_beats(monitor_id, period=24)`: Get monitor heartbeat data

#### Notification Management

- `await add_notification(notification_data)`: Add a notification
- `await delete_notification(notification_id)`: Delete a notification
- `await test_notification(notification_data)`: Test a notification

#### Status Page Management

- `await add_status_page(title, slug)`: Create a status page
- `await save_status_page(slug, config, public_group_list)`: Save status page config
- `await delete_status_page(slug)`: Delete a status page

#### Event Handlers

- `on_heartbeat(callback)`: Register heartbeat event callback
- `on_monitor_list_update(callback)`: Register monitor list update callback
- `on_uptime_update(callback)`: Register uptime update callback

### UptimeKumaRESTClient

REST API client for basic operations.

#### Initialization

```python
client = UptimeKumaRESTClient(
    base_url="http://localhost:3001",
    username="your_username",    # Optional
    password="your_password",    # Optional
    api_key="your_api_key"       # Optional
)
```

#### Methods

- `push_monitor_status(push_token, status="up", msg="OK", ping=None)`: Push monitor status
- `get_status_page(slug)`: Get status page data
- `get_status_page_heartbeat(slug)`: Get status page heartbeat data
- `get_metrics()`: Get Prometheus metrics
- `get_entry_page()`: Get entry page information

## Monitor Types

Uptime Kuma supports various monitor types:

| Type | Description |
|------|-------------|
| `http` | HTTP/HTTPS website monitoring |
| `keyword` | Monitor for specific text content |
| `ping` | ICMP ping monitoring |
| `port` | TCP port monitoring |
| `dns` | DNS resolution monitoring |
| `push` | Push-based monitoring |
| `steam` | Steam game server monitoring |
| `docker` | Docker container monitoring |

## Authentication

The library supports multiple authentication methods:

1. **Username/Password**: Traditional login credentials
2. **API Key**: For metrics endpoint access
3. **JWT Token**: For token-based authentication after initial login

## Error Handling

```python
from uptime_kuma_api import UptimeKumaClient
import asyncio

async def main():
    client = UptimeKumaClient(base_url="http://localhost:3001")

    try:
        await client.connect()
        result = await client.login("username", "password")

        if not result.get("ok"):
            print(f"Login failed: {result.get('msg')}")
            return

        # Your code here

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()
```

## Examples

See the `examples/` directory for complete usage examples:

- `basic_monitoring.py`: Basic monitor creation and management
- `real_time_events.py`: Real-time event handling
- `status_page_monitoring.py`: Status page data retrieval
- `notification_setup.py`: Notification configuration

## Development

### Setup Development Environment

```bash
git clone https://github.com/emadomedher/pyKumaAPI.git
cd pyKumaAPI
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library is not officially affiliated with or endorsed by the Uptime Kuma project. Uptime Kuma's API is internal and may change without notice. Use this library at your own risk.

## Support

- 📖 [Documentation](https://github.com/emadomedher/pyKumaAPI#readme)
- 🐛 [Bug Reports](https://github.com/emadomedher/pyKumaAPI/issues)
- 💬 [Discussions](https://github.com/emadomedher/pyKumaAPI/discussions)

## Changelog

### [0.1.0] - 2025-11-03
- Initial release
- REST API client implementation
- Socket.io real-time client implementation
- Comprehensive monitor management
- Event handling system
- Multiple authentication methods
