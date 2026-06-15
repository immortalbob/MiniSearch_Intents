# MiniSearch Intents

A Home Assistant custom integration that exposes [MiniSearch](https://github.com/immortalbob/MiniSearch) as a native LLM tool API, available to any LLM-backed conversation agent (Ollama, OpenAI, etc.) directly from the HA UI.

Once installed, MiniSearch Intents appears as a selectable API in your conversation agent options alongside the built-in Assist API. Your LLM can then search across your entire local knowledge stack and perform utility functions with a single tool call.

## Tools

| Tool | Description | Status |
|------|-------------|--------|
| `minisearch` | Routes queries to Kiwix, Open-Meteo, FreshRSS, or SearXNG | ✅ Tested |
| `calculator` | Evaluates math expressions, sqrt, trig, average | ✅ Tested |
| `unit_converter` | Converts between kitchen, weight, length, data, speed, and temperature units | ✅ Tested |
| `calendar_day` | Returns day of week and relative info for a given date | ✅ Tested |
| `set_timer` | Sets a timer that announces via TTS on the originating satellite | ⚠️ Untested — may conflict with built-in Assist timer handling |

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

## Unit Converter reference

Supported unit pairs:

- **Kitchen volume:** cup, tablespoon, teaspoon, ml, pint, liter
- **Weight:** kg, lb, oz, g
- **Length:** km, mile, m, ft, inch, cm
- **Data:** kb, mb, gb, tb
- **Speed:** mph, kph
- **Temperature:** use `celsius_to_fahrenheit` or `fahrenheit_to_celsius` as the `from_unit`

Amounts can be fractions: `1/2`, `1 1/2`, `0.75`

## Part of the MiniNet stack

- [MiniSearch](https://github.com/immortalbob/MiniSearch) — the search backend
- [openwebui-tools](https://github.com/immortalbob/openwebui-tools) — Open WebUI tool versions of the same sources
