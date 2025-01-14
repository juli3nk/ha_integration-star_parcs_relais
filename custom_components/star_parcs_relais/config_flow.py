"""Config flow for the Star Parcs Relais integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class StarParcsRelaisConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Star Parcs Relais."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step initiated by the user."""

        return self.async_create_entry(
            title="STAR Parcs Relais",
            data={},  # Pas de données à enregistrer
        )
