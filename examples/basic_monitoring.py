#!/usr/bin/env python3
"""
Basic Uptime Kuma monitoring example.

This example demonstrates how to connect to Uptime Kuma, authenticate,
and perform basic monitor management operations.
"""

import asyncio
from uptime_kuma_api import UptimeKumaClient


async def main():
    # Initialize the client
    client = UptimeKumaClient(
        base_url="http://localhost:3001",
        username="admin",
        password="password"
    )

    try:
        # Connect to Uptime Kuma
        print("Connecting to Uptime Kuma...")
        connected = await client.connect()
        if not connected:
            print("❌ Failed to connect to Uptime Kuma")
            return

        print("✅ Connected successfully")

        # Authenticate
        print("Authenticating...")
        login_result = await client.login("admin", "password")
        if not login_result.get("ok"):
            print(f"❌ Login failed: {login_result.get('msg')}")
            return

        print("✅ Authentication successful")

        # Get existing monitors
        print("Fetching monitors...")
        monitors = await client.get_monitor_list()
        print(f"📊 Found {len(monitors)} monitors")

        # Create a new HTTP monitor
        print("Creating new HTTP monitor...")
        monitor_data = {
            "name": "Example Website",
            "type": "http",
            "url": "https://httpbin.org/status/200",
            "interval": 60,  # Check every 60 seconds
            "timeout": 30,   # 30 second timeout
            "active": True
        }

        create_result = await client.add_monitor(monitor_data)
        if create_result.get("ok"):
            monitor_id = create_result.get("monitorID")
            print(f"✅ Monitor created with ID: {monitor_id}")

            # Wait a moment then pause the monitor
            await asyncio.sleep(2)
            print("Pausing monitor...")
            pause_result = await client.pause_monitor(monitor_id)
            if pause_result.get("ok"):
                print("✅ Monitor paused")

                # Resume the monitor
                await asyncio.sleep(1)
                print("Resuming monitor...")
                resume_result = await client.resume_monitor(monitor_id)
                if resume_result.get("ok"):
                    print("✅ Monitor resumed")

            # Get monitor details
            print("Fetching monitor details...")
            monitor_details = await client.get_monitor(monitor_id)
            if monitor_details.get("ok"):
                monitor = monitor_details.get("monitor", {})
                print(f"📋 Monitor details: {monitor.get('name')} - {monitor.get('active', 'Unknown status')}")

        else:
            print(f"❌ Failed to create monitor: {create_result.get('msg')}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # Clean up
        print("Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
