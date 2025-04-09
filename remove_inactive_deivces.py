import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()

TAILSCALE_API_KEY = os.getenv("TAILSCALE_API_KEY")
TAILSCALE_ACCOUNT_NAME = os.getenv("TAILSCALE_ACCOUNT_NAME")

TAILSCALE_API_URL = f"https://api.tailscale.com/api/v2/tailnet/{TAILSCALE_ACCOUNT_NAME}/devices"
TAILSCALE_API_URL_DEL = "https://api.tailscale.com/api/v2/device"

# Set the threshold for inactivity (in minutes)
INACTIVITY_THRESHOLD = 5  # 60 minutes

# Headers to authenticate the API request
headers = {
    "Authorization": f"Bearer {TAILSCALE_API_KEY}",
    "Content-Type": "application/json",
}

# List all devices
def list_devices():
    response = requests.get(TAILSCALE_API_URL, headers=headers)
    if response.status_code == 200:
        devices = response.json()['devices']
        return devices
    else:
        print(f"Failed to fetch devices. Status code: {response.status_code}")
        return []

# Remove a device
def remove_device(device_id):
    response = requests.delete(f"{TAILSCALE_API_URL_DEL}/{device_id}", headers=headers)
    if response.status_code == 200:
        print(f"Device {device_id} removed successfully.")
    else:
        print(f"Failed to remove device {device_id}. Status code: {response.status_code}")

# Check inactivity and remove devices
def remove_inactive_devices(devices):
    now = datetime.now(timezone.utc)

    for device in devices:
        
        IPv4 = device.get('addresses')[0]
        last_seen = device.get('lastSeen')
        hostname = device.get('hostname')
        #print(IPv4, hostname,last_seen)

        if last_seen:
            last_seen_time = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))  # Ensure UTC-aware
            time_diff = now - last_seen_time
            
            if time_diff > timedelta(minutes=INACTIVITY_THRESHOLD):
                print(f"Device {IPv4}, {hostname} inactive for { round(time_diff.total_seconds()/60) } minutes, has been removed")
                remove_device(device['id'])
        else:
            print(f"Device {IPv4}, {hostname} does not have the lastSeen timestamp.")

def main():
    devices = list_devices()
    if devices:
        remove_inactive_devices(devices)
    else:
        print("No devices found.")

if __name__ == "__main__":
    main()
