#!/usr/bin/env python3
"""
Real-time event handling example for Uptime Kuma.

This example demonstrates how to handle real-time events such as heartbeats,
monitor updates, and uptime changes using callbacks.
"""

import asyncio
from uptime_kuma_api import UptimeKumaClient
import json


def format_heartbeat(data):
    """Format heartbeat data for display."""
    monitor_id = data.get('monitorID')
    status = data.get('status')
    ping = data.get('ping')
    msg = data.get('msg', '')

    status_text = {
        0: "🔴 DOWN",
        1: "🟢 UP",
        2: "🟡 PENDING",
        3: "🟠 MAINTENANCE"
    }.get(status, f"UNKNOWN({status})")

    ping_text = f" ({ping}ms)" if ping else ""

    return f"Monitor {monitor_id}: {status_text}{ping_text} - {msg}"


async def on_heartbeat(data):
    """Handle heartbeat events."""
    print(f"💓 Heartbeat: {format_heartbeat(data)}")


async def on_monitor_list_update(data):
    """Handle monitor list updates."""
    print(f"📋 Monitor list updated: {len(data)} monitors")
    for monitor_id, monitor in data.items():
        name = monitor.get('name', 'Unknown')
        active = "Active" if monitor.get('active') else "Inactive"
        print(f"  • {monitor_id}: {name} ({active})")


async def on_uptime_update(data):
    """Handle uptime updates."""
    monitor_id = data.get('monitorID')
    period = data.get('periodKey', 'unknown')
    percentage = data.get('percentage', 0)
    print(f"📈 Uptime update: Monitor {monitor_id} - {period}: {percentage:.2f}%")


async def main():
    # Initialize the client
    client = UptimeKumaClient(
        base_url="http://localhost:3001",
        username="admin",
        password="password"
    )

    # Register event handlers
    client.on_heartbeat(on_heartbeat)
    client.on_monitor_list_update(on_monitor_list_update)
    client.on_uptime_update(on_uptime_update)

    try:
        # Connect to Uptime Kuma
        print("🔌 Connecting to Uptime Kuma...")
        connected = await client.connect()
        if not connected:
            print("❌ Failed to connect")
            return

        print("✅ Connected successfully")

        # Authenticate
        print("🔐 Authenticating...")
        login_result = await client.login("admin", "password")
        if not login_result.get("ok"):
            print(f"❌ Login failed: {login_result.get('msg')}")
            return

        print("✅ Authentication successful")
        print("🎧 Listening for real-time events... (Press Ctrl+C to stop)")

        # Keep the connection alive and listen for events
        # In a real application, you might want to run this indefinitely
        await asyncio.sleep(300)  # Listen for 5 minutes

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        print("🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected")


async def demo_with_manual_events():
    """
    Demonstration of how events work by manually triggering some operations.
    This is useful for testing event handlers without waiting for real events.
    """
    client = UptimeKumaClient(
        base_url="http://localhost:3001",
        username="admin",
        password="password"
    )

    # Register event handlers
    client.on_heartbeat(on_heartbeat)
    client.on_monitor_list_update(on_monitor_list_update)
    client.on_uptime_update(on_uptime_update)

    try:
        connected = await client.connect()
        if not connected:
            return

        login_result = await client.login("admin", "password")
        if not login_result.get("ok"):
            return

        print("🎯 Performing operations to trigger events...")

        # Create a monitor to trigger events
        monitor_data = {
            "name": "Demo Monitor",
            "type": "http",
            "url": "https://httpbin.org/status/200",
            "interval": 30,
            "active": True
        }

        create_result = await client.add_monitor(monitor_data)
        if create_result.get("ok"):
            monitor_id = create_result.get("monitorID")
            print(f"✅ Created monitor {monitor_id}")

            # Wait for some heartbeats
            print("⏳ Waiting for heartbeats...")
            await asyncio.sleep(10)

            # Pause and resume to trigger more events
            await client.pause_monitor(monitor_id)
            await asyncio.sleep(2)
            await client.resume_monitor(monitor_id)
            await asyncio.sleep(10)

            # Clean up
            await client.delete_monitor(monitor_id)
            print("🗑️ Cleaned up demo monitor")

        await asyncio.sleep(5)  # Wait for final events

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    print("Choose an example:")
    print("1. Listen for real-time events")
    print("2. Demo with manual operations")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "2":
        asyncio.run(demo_with_manual_events())
    else:
        asyncio.run(main())
