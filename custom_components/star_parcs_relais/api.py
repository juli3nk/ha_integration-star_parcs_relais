"""Récupère les données des parkings relais STAR de Rennes Métropole via l'API."""

import aiohttp

API_URL = "https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/tco-parcsrelais-star-etat-tr/records?limit=20"


async def fetch_parking_data():
    """Cette fonction effectue une requête asynchrone à l'API publique et récupère
    les informations sur l'état des parkings relais.

    Returns:
        list: Une liste de dictionnaires contenant les données des parkings relais.

    Raises:
        Exception: Si la requête HTTP échoue ou si l'API ne répond pas avec un statut 200.
    """

    async with (
        aiohttp.ClientSession() as session,
        session.get(API_URL) as response,
    ):
        if response.status == 200:
            data = await response.json()

            return data["results"]
        else:
            raise Exception("Erreur lors de la récupération des données STAR")
