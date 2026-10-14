# SafeStride — Smart Safety Anklet

**Team:** TRINEX  
**Theme:** Healthcare & Wellbeing  
**Prototype type:** Software simulation of an emergency-alert workflow

SafeStride is a concept for a discreet wearable anklet that can trigger an SOS alert, attach a location, and activate a local alarm. This repository provides a beginner-friendly software prototype that simulates the workflow without requiring physical GPS/GSM hardware.

## Features in this prototype

- Simulates a double-tap emergency trigger.
- Reads demo GPS coordinates from sample data or environment variables.
- Creates an SOS alert record in JSON format.
- Simulates a buzzer/LED status in the console.
- Includes sample data and automated tests.

> **Important limitation:** This is a software simulation, not a validated safety device. It does not send a real SMS, obtain live GPS, or control a physical buzzer/LED. Do not rely on it for emergencies. Real hardware, secure contact configuration, field testing, and safety review are required.

## Project structure

```text
TRINEX_SafeStride_Repository/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── TECHNICAL_DESIGN.md
├── src/
│   └── safestride.py
├── sample_data/
│   ├── demo_location.json
│   └── sample_alert.json
└── tests/
    └── test_safestride.py
```

## Requirements

- Python 3.10 or newer
- No third-party Python packages are required

## Setup

### Windows
1. Install Python from https://www.python.org/downloads/ . During installation, select **Add Python to PATH**.
2. Download this repository as a ZIP from GitHub and extract it.
3. Open the extracted folder.
4. Open Command Prompt in that folder.
5. Run:

```bash
python src/safestride.py
```

### Android phone
You can upload and store the repository on GitHub using your browser. Running Python on Android requires a separate Python environment app and may vary by device; the simplest reliable test is on a laptop/desktop with Python installed.

## Run the simulation

```bash
python src/safestride.py
```

The program prints a simulated SOS alert and saves it to `output/alerts.json`.

To provide a demo location through environment variables:

**Windows Command Prompt**
```bat
set SAFESTRIDE_LAT=12.9716
set SAFESTRIDE_LON=80.2209
python src/safestride.py
```

**macOS/Linux**
```bash
export SAFESTRIDE_LAT=12.9716
export SAFESTRIDE_LON=80.2209
python src/safestride.py
```

Optional variables:
- `SAFESTRIDE_LAT` — demo latitude; defaults to the sample location.
- `SAFESTRIDE_LON` — demo longitude; defaults to the sample location.
- `SAFESTRIDE_CONTACT` — label for the intended emergency contact; defaults to `Demo Contact`. This prototype does not actually contact them.
- `SAFESTRIDE_OUTPUT` — output JSON path; defaults to `output/alerts.json`.

Never commit private phone numbers, passwords, API keys, or personal location data to a public repository.

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests check alert creation, coordinates, and invalid coordinate handling.

## Expected demo output

The console reports that an SOS event was simulated and that buzzer/LED indicators would activate. The alert record is written to `output/alerts.json`.

## Hardware integration roadmap

1. Replace the simulated trigger with a suitable double-tap/touch sensor input.
2. Read real coordinates from a GPS module.
3. Connect a GSM module and test SMS delivery using a dedicated test SIM and consented contacts.
4. Drive a buzzer and LED through suitable driver circuitry.
5. Add battery protection, waterproofing, enclosure testing, and fail-safe behavior.
6. Test thoroughly before making any real-world safety claims.

## License

Released under the MIT License. See `LICENSE`.
