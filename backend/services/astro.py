import os
from datetime import date
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

try:
    from backend.data.city_fallback import fallback_geo_search
except ModuleNotFoundError:
    from data.city_fallback import fallback_geo_search

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=False)

FREEASTRO_BASE_URL = os.getenv("FREEASTRO_BASE_URL", "https://api.freeastroapi.com")
FREEASTRO_API_KEY = os.getenv("FREEASTRO_API_KEY", "")


def _headers() -> dict[str, str]:
    return {"x-api-key": FREEASTRO_API_KEY}


async def search_geo(query: str) -> list[dict]:
    if not FREEASTRO_API_KEY or FREEASTRO_API_KEY == "your_freeastroapi_key":
        return fallback_geo_search(query)

    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                f"{FREEASTRO_BASE_URL}/api/v2/geo/search",
                params={"q": query},
                headers=_headers(),
            )
            response.raise_for_status()
            payload = response.json()
            items = payload.get("data", payload if isinstance(payload, list) else [])
            results = [
                {
                    "city_name": item.get("city_name") or item.get("name") or item.get("city") or "",
                    "state": item.get("state") or "",
                    "country": item.get("country") or "",
                    "lat": item.get("lat") or item.get("latitude"),
                    "lng": item.get("lng") or item.get("longitude"),
                    "tz_str": item.get("tz_str") or item.get("timezone") or "",
                }
                for item in items
            ]
            return results or fallback_geo_search(query)
    except httpx.HTTPError:
        return fallback_geo_search(query)


async def calculate_vedic_chart(payload: dict) -> dict:
    if not FREEASTRO_API_KEY or FREEASTRO_API_KEY == "your_freeastroapi_key":
        raise HTTPException(status_code=503, detail="FreeAstroAPI key is not configured.")

    body = {
        **payload,
        "ayanamsha": "lahiri",
        "house_system": "whole_sign",
        "node_type": "mean",
        "include_yogas": True,
        "include_shadbala": True,
        "include_panchang": True,
        "dasha_levels": 1,
        "reference_date": date.today().isoformat(),
    }

    async with httpx.AsyncClient(timeout=18) as client:
        response = await client.post(
            f"{FREEASTRO_BASE_URL}/api/v2/vedic/calculate",
            json=body,
            headers=_headers(),
        )
        response.raise_for_status()
        return response.json()
