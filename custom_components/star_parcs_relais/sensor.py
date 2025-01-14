"""Sensor for the Star Parcs Relais integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import COORDINATOR, DOMAIN
from .coordinator import StarParcsRelaisConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: StarParcsRelaisConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors for the STAR Parcs relais integration."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    sensors = []

    # Parcourir les données et créer un capteur pour chaque parc relais
    for park in coordinator.data:
        sensors.append(StarParcsRelaisSensor(park["nom"], coordinator))

    async_add_entities(sensors, True)


class StarParcsRelaisSensor(SensorEntity):
    """Sensor for a specific parc relais."""

    def __init__(self, park_name, coordinator):
        """Initialize the sensor."""
        self._park_name = park_name
        self.coordinator = coordinator
        self._state = None

    @property
    def name(self):
        """Name of the sensor."""
        return f"STAR Parc relais {self._park_name}"

    @property
    def state(self):
        """Main state (opening status)."""
        park_data = self._get_park_data()
        return park_data["etatouverture"] if park_data else None

    @property
    def extra_state_attributes(self):
        """Additional attributes."""
        park_data = self._get_park_data()
        if not park_data:
            return {}
        return {
            "id": park_data["idparc"],
            "nom": park_data["nom"],
            "longitude": park_data["coordonnees"]["lon"],
            "latitude": park_data["coordonnees"]["lat"],
            "etat_ouverture": park_data["etatouverture"],
            "etat_remplissage": park_data["etatremplissage"],
            "jrd_mention_ligne1": park_data["jrdmentionligne1"],
            "jrd_mention_ligne2": park_data["jrdmentionligne2"],
            "last_update": park_data["lastupdate"],
            "capacite": park_data["capaciteparking"],
            "capacite_soliste": park_data["capacitesoliste"],
            "jrd_info_soliste": park_data["jrdinfosoliste"],
            "capacite_electrique": park_data["capaciteve"],
            "jrd_info_electrique": park_data["jrdinfoelectrique"],
            "capacite_covoiturage": park_data["capacitecovoiturage"],
            "jrd_info_covoiturage": park_data["jrdinfocovoiturage"],
            "capacite_pmr": park_data["capacitepmr"],
            "jrd_info_pmr": park_data["jrdinfopmr"],
        }

    @property
    def icon(self):
        """Icon for the sensor."""
        return "mdi:parking"

    def _get_park_data(self):
        """Retrieve data for this parc relais."""
        for park in self.coordinator.data:
            if park["nom"] == self._park_name:
                return park
        return None

    async def async_update(self):
        """Ask the coordinator to update the data."""
        await self.coordinator.async_request_refresh()
