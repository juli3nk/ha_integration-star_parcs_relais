"""Coordinator for the Star Parcs Relais integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import fetch_parking_data
from .const import _LOGGER, DOMAIN, UPDATE_INTERVAL

type StarParcsRelaisConfigEntry = ConfigEntry[StarParcsRelaisDataUpdateCoordinator]


class StarParcsRelaisDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for retrieving and updating Parcs Relais STAR data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Retrieve data from the Star API."""
        try:
            return await fetch_parking_data()
        except Exception as err:
            _LOGGER.error(
                "Erreur lors de la mise à jour des données STAR Parcs Relais: %s", err
            )
            raise
