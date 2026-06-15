"""MiniSearch Intents — LLM tool integration for Home Assistant."""
from __future__ import annotations

import logging
import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import llm
from homeassistant.util.json import JsonObjectType

from .const import DOMAIN, CONF_MINISEARCH_URL, DEFAULT_MINISEARCH_URL, API_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MiniSearch Intents from a config entry."""
    url = entry.options.get(
        CONF_MINISEARCH_URL,
        entry.data.get(CONF_MINISEARCH_URL, DEFAULT_MINISEARCH_URL),
    )

    unreg = llm.async_register_api(
        hass,
        MiniSearchAPI(
            hass=hass,
            id=f"{DOMAIN}-{entry.entry_id}",
            name=API_NAME,
            minisearch_url=url,
        ),
    )
    entry.async_on_unload(unreg)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update — reload to re-register API with new URL."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload MiniSearch Intents config entry."""
    return True


class MiniSearchAPI(llm.API):
    """MiniSearch LLM API — exposes MiniSearch as a tool to HA conversation agents."""

    def __init__(
        self,
        hass: HomeAssistant,
        id: str,
        name: str,
        minisearch_url: str,
    ) -> None:
        super().__init__(hass=hass, id=id, name=name)
        self.minisearch_url = minisearch_url

    async def async_get_api_instance(
        self, llm_context: llm.LLMContext
    ) -> llm.APIInstance:
        """Return an API instance with the MiniSearch tool."""
        return llm.APIInstance(
            api=self,
            api_prompt=(
                "You have access to MiniSearch, a unified local knowledge search tool. "
                "Use the `minisearch` tool to look up information when answering questions. "
                "MiniSearch will automatically route your query to the best available source: "
                "offline knowledge base (Wikipedia, Stack Exchange, iFixit, FreeCodeCamp), "
                "3-day weather forecast, recent RSS news articles, or live web search. "
                "You can also specify a source explicitly using the `source` parameter: "
                "'kiwix' for offline knowledge, 'forecast' for weather, "
                "'news' for RSS articles, or 'web' for live web search. "
                "Use 'auto' or omit the source to let MiniSearch decide."
            ),
            llm_context=llm_context,
            tools=[MiniSearchTool(self.minisearch_url)],
        )


class MiniSearchTool(llm.Tool):
    """Tool that queries the MiniSearch container."""

    name = "minisearch"
    description = (
        "Search for information using MiniSearch. Automatically selects the best source "
        "based on the query — offline knowledge base, weather forecast, news feed, or web search. "
        "Use source='forecast' for weather questions, source='news' for recent articles, "
        "source='kiwix' for encyclopedic or technical knowledge, source='web' for current events. "
        "Leave source as 'auto' when unsure."
    )
    parameters = vol.Schema({
        vol.Required("query"): str,
        vol.Optional("source", default="auto"): vol.In(
            ["auto", "kiwix", "forecast", "news", "web"]
        ),
    })

    def __init__(self, minisearch_url: str) -> None:
        self.minisearch_url = minisearch_url

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: llm.ToolInput,
        llm_context: llm.LLMContext,
    ) -> JsonObjectType:
        """Call MiniSearch and return the result."""
        query = tool_input.tool_args["query"]
        source = tool_input.tool_args.get("source", "auto")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.minisearch_url}/search",
                    json={"query": query, "source": source},
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status != 200:
                        raise HomeAssistantError(
                            f"MiniSearch returned HTTP {resp.status}"
                        )
                    data = await resp.json()
                    return {
                        "result": data.get("result", "No result returned."),
                        "source_used": data.get("source_used", source),
                    }
        except aiohttp.ClientConnectorError as err:
            raise HomeAssistantError(
                f"Cannot connect to MiniSearch at {self.minisearch_url}: {err}"
            ) from err
        except aiohttp.ClientError as err:
            raise HomeAssistantError(f"MiniSearch request failed: {err}") from err
