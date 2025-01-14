"""The Star Parcs Relais integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import _LOGGER, COORDINATOR, DOMAIN
from .coordinator import StarParcsRelaisConfigEntry, StarParcsRelaisDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

# async def async_setup(hass: HomeAssistant, config: dict) -> bool:
#     """Configure l'intégration via configuration.yaml (non utilisé ici)."""
#     return True

async def async_setup_entry(
    hass: HomeAssistant,
    entry: StarParcsRelaisConfigEntry,
) -> bool:
    """Set up Star Parcs Relais from a config entry."""

    # Créer un DataUpdateCoordinator pour gérer les mises à jour périodiques des données
    coordinator = StarParcsRelaisDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    # Stocker le coordinator dans l'objet hass
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator,
    }

    # Charger les plateformes (ex. : sensor.py)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Déchargement de l'entrée %s", entry.title)

    # Décharger les plateformes
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Nettoyer les données stockées
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
