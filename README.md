# Mnemolis Intents

A Home Assistant custom integration that exposes [Mnemolis](https://github.com/immortalbob/Mnemolis) as a native LLM Tool API, making it available to any LLM-backed conversation agent (Ollama, OpenAI, Anthropic, etc.) directly from the HA UI.

Once installed, Mnemolis appears as a selectable API in your conversation agent options alongside the built-in Assist API. Your LLM can then search across your entire local knowledge stack with a single tool call.

## What Mnemolis provides

- **Offline knowledge** — Wikipedia, Stack Exchange, iFixit, FreeCodeCamp, DevDocs via Kiwix
- **Weather forecast** — 3-day forecast via Open-Meteo (no API key required)
- **News** — Recent articles from your FreshRSS RSS feeds
- **Web search** — Live search via your local SearXNG instance
- **Service status** — Monitor status for all services via Uptime Kuma
- **Home Assistant** — Entity state summaries — lights, locks, sensors, motion, batteries, power

## Available Tools

| Tool | Description | Status |
|------|-------------|--------|
| `mnemolis` | Routes queries to Kiwix, Open-Meteo, FreshRSS, SearXNG, Uptime Kuma, or Home Assistant | ✅ Working |
| `calculator` | Evaluates math expressions, sqrt, trig, average | ✅ Working |
| `unit_converter` | Converts between kitchen, weight, length, data, speed, and temperature units | ✅ Working |
| `calendar_day` | Returns day of week and relative info for a given date | ✅ Working |

## Requirements

- [Mnemolis](https://github.com/immortalbob/Mnemolis) v3.2.0 or later running and reachable from Home Assistant
- Home Assistant 2024.6.0 or later
- An LLM conversation agent (Ollama, OpenAI, etc.) configured in Home Assistant

## Installation

### Via HACS (recommended)

1. Add this repository as a custom repository in HACS (type: Integration)
2. Install **Mnemolis Intents**
3. Restart Home Assistant

### Manual

1. Copy `custom_components/mnemolis_intents` to your HA `custom_components` directory
2. Restart Home Assistant

## Setup

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Mnemolis Intents**
3. Enter your Mnemolis URL (e.g. `http://192.168.3.5:8888`)
4. Click Submit — HA will verify the connection before saving

## Enabling for your conversation agent

1. Go to **Settings → Devices & Services**
2. Find your conversation agent (e.g. Ollama)
3. Click **Configure**
4. Under **Control Home Assistant**, enable **Mnemolis**
5. Save

Your LLM will now have access to the `mnemolis` tool and will use it automatically when answering questions that require looking things up.

## Calculator

Supports standard arithmetic, exponents, square roots, trig functions, and averages.

Examples:
- `what is the square root of 1764`
- `what is average of 10, 20, 30`
- `what is sin of 45`

## Unit Converter

Supported unit pairs:

- **Kitchen volume:** cup, tablespoon, teaspoon, ml, pint, liter
- **Weight:** kg, lb, oz, g
- **Length:** km, mile, m, ft, inch, cm
- **Data:** kb, mb, gb, tb
- **Speed:** mph, kph, mps (meters per second)
- **Temperature:** use `from_unit='c'` `to_unit='f'` or `from_unit='f'` `to_unit='c'`

Amounts can be fractions: `1/2`, `1 1/2`, `0.75`

## Calendar Day

Ask what day of the week a date falls on, or how many days until an event.

Examples:
- `what day is July 4th`
- `how many days until Christmas`
- `what day was January 1st 2000`

## Compatibility

| Mnemolis Intents | Mnemolis |
|-----------------|----------|
| v1.3.0 | v3.2.0 or later |
| v1.2.0 | v2.3.0 or later |
| v1.1.0 | v2.0.0 or later |

## Part of the MiniNet stack

- [Mnemolis](https://github.com/immortalbob/Mnemolis) — the knowledge broker backend
- [MiniSense-T7S3](https://github.com/immortalbob/MiniSense-T7S3) — ESP32-S3 room sensor node with voice assistant and CO2 monitoring
