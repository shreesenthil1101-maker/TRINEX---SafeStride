"""SafeStride software simulation. No real GPS, SMS, buzzer, or LED hardware is used."""
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_LOCATION = ROOT / "sample_data" / "demo_location.json"


def validate_coordinates(latitude, longitude):
    """Validate latitude/longitude and return a normalized tuple of floats."""
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (TypeError, ValueError) as exc:
        raise ValueError("Latitude and longitude must be numeric.") from exc
    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180.")
    return lat, lon


def get_demo_location():
    """Get demo coordinates from environment variables or the sample JSON file."""
    lat_env = os.getenv("SAFESTRIDE_LAT")
    lon_env = os.getenv("SAFESTRIDE_LON")
    if lat_env is not None or lon_env is not None:
        if lat_env is None or lon_env is None:
            raise ValueError("Set both SAFESTRIDE_LAT and SAFESTRIDE_LON.")
        return validate_coordinates(lat_env, lon_env)

    with SAMPLE_LOCATION.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return validate_coordinates(data["latitude"], data["longitude"])


def create_sos_alert(latitude, longitude, contact_label="Demo Contact"):
    """Build an SOS alert object; this does not send a message."""
    lat, lon = validate_coordinates(latitude, longitude)
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event_type": "SOS",
        "status": "SIMULATED",
        "location": {"latitude": lat, "longitude": lon},
        "contact_label": contact_label,
        "indicators": {"buzzer": "SIMULATED_ON", "led": "SIMULATED_ON"},
    }


def save_alert(alert, output_path):
    """Append an alert record to a JSON array file."""
    path = Path(output_path)
    if not path.is_absolute():
        path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except (json.JSONDecodeError, OSError):
            existing = []
    else:
        existing = []
    existing.append(alert)
    path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return path


def main():
    latitude, longitude = get_demo_location()
    contact = os.getenv("SAFESTRIDE_CONTACT", "Demo Contact")
    output_path = os.getenv("SAFESTRIDE_OUTPUT", "output/alerts.json")
    alert = create_sos_alert(latitude, longitude, contact)
    print("SafeStride: double-tap trigger SIMULATED.")
    print(f"SOS status: {alert['status']}")
    print(f"Demo location: {latitude}, {longitude}")
    print(f"Contact label: {contact} (no message sent)")
    print("Buzzer: SIMULATED_ON | LED: SIMULATED_ON")
    saved_to = save_alert(alert, output_path)
    print(f"Alert record saved to: {saved_to}")
    print("Reminder: this is a software demo, not a real emergency-alert device.")


if __name__ == "__main__":
    main()
