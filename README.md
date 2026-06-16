# MiniSearch Intents

A Home Assistant custom integration that exposes [MiniSearch](https://github.com/immortalbob/MiniSearch) as a native LLM tool API, available to any LLM-backed conversation agent (Ollama, OpenAI, etc.) directly from the HA UI.

Once installed, MiniSearch Intents appears as a selectable API in your conversation agent options alongside the built-in Assist API. Your LLM can then search across your entire local knowledge stack and perform utility functions with a single tool call.

## Tools

| Tool | Description | Status |
|------|-------------|--------|
| `minisearch` | Routes queries to Kiwix, Open-Meteo, FreshRSS, or SearXNG | ✅ Working |
| `calculator` | Evaluates math expressions, sqrt, trig, average | ✅ Working |
| `unit_converter` | Converts between kitchen, weight, length, data, speed, and temperature units | ✅ Working |
| `calendar_day` | Returns day of week and relative info for a given date | ✅ Working |
| `set_timer` | Sets a timer that announces via TTS on the originating satellite | ⚠️ Work in progress — conflicts with built-in Assist timer handling |
| Compound unit conversion | Handles inputs like "5 ft 10 in" or "2 lb 4 oz" | ⚠️ Work in progress — 8B models tend to pre-convert before calling the tool |

## What MiniSearch provides

- **Offline knowledge** — Wikipedia, Stack Exchange, iFixit, FreeCodeCamp, DevDocs via Kiwix
- **Weather forecast** — 3-day forecast via Open-Meteo (no API key required)
- **News** — Recent articles from your FreshRSS RSS feeds
- **Web search** — Live search via your local SearXNG instance

## Requirements

- [MiniSearch](https://github.com/immortalbob/MiniSearch) running and reachable from Home Assistant
- Home Assistant 2024.6.0 or later
- An LLM conversation agent (Ollama, OpenAI, etc.) configured in Home Assistant

## Installation

### Via HACS (recommended)

1. Add this repository as a custom repository in HACS (type: Integration)
2. Install **MiniSearch Intents**
3. Restart Home Assistant

### Manual

1. Copy `custom_components/minisearch_intents` to your HA `custom_components` directory
2. Restart Home Assistant

## Setup

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **MiniSearch Intents**
3. Enter your MiniSearch URL (e.g. `http://192.168.3.5:8888`)
4. Click Submit — HA will verify the connection before saving

## Enabling for your conversation agent

1. Go to **Settings → Devices & Services**
2. Find your conversation agent (e.g. Ollama)
3. Click **Configure**
4. Under **Control Home Assistant**, enable **MiniSearch**
5. Save

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
- **Speed:** mph, kph
- **Temperature:** use `celsius_to_fahrenheit` or `fahrenheit_to_celsius` as the `from_unit`

Amounts can be fractions: `1/2`, `1 1/2`, `0.75`

Compound amounts are supported in the tool schema (`5 ft 10 in`, `2 lb 4 oz`) but smaller LLMs (8B) tend to pre-convert to a single unit before calling the tool, bypassing this feature. Works more reliably with larger models.

## Calendar Day

Ask what day of the week a date falls on, or how many days until an event.

Examples:
- `what day is July 4th`
- `how many days until Christmas`
- `what day was January 1st 2000`

## Timer

Sets a timer that announces via TTS when done. Currently conflicts with Home Assistant's built-in Assist timer handling on some setups — under investigation.

## Part of the MiniNet stack

- [MiniSearch](https://github.com/immortalbob/MiniSearch) — the search backend
- [openwebui-tools](https://github.com/immortalbob/openwebui-tools) — Open WebUI tool versions of the same sources
