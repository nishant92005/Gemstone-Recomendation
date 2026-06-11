import asyncio
import json
import logging
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

try:
    from backend.services.astro import calculate_vedic_chart
    from backend.services.chart_parser import parse_chart
    from backend.services.groq_service import generate_reading
except ModuleNotFoundError:
    from services.astro import calculate_vedic_chart
    from services.chart_parser import parse_chart
    from services.groq_service import generate_reading

router = APIRouter(prefix="/api", tags=["consult"])
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "gemstone_kb.json"


class ConsultRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    tz_str: str = Field(..., min_length=1)


def load_gemstones() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def build_analysis_sections(chart: dict) -> list[dict]:
    strengths = sorted(chart["shadbala"].items(), key=lambda item: item[1])
    weakest = strengths[:3]
    strongest = [item for item in reversed(strengths) if item[0] in chart["strong_planets"]][:3]

    return [
        {
            "title": "Chart Snapshot",
            "items": [
                f"Lagna: {chart['lagna']['sign'] or 'Not reported'}",
                f"Nakshatra: {chart['lagna']['nakshatra'] or 'Not reported'}",
                f"Current Mahadasha: {chart['mahadasha_lord'] or 'Not reported'}",
                f"Sade Sati Active: {'Yes' if chart['sade_sati'] else 'No'}",
            ],
        },
        {
            "title": "Weak Planet Signals",
            "items": [
                f"{planet}: Shadbala ratio {ratio}"
                for planet, ratio in weakest
            ],
        },
        {
            "title": "Strong Planet Signals",
            "items": [
                f"{planet}: Shadbala ratio {ratio}"
                for planet, ratio in strongest
            ] or ["No strongly amplified planet was identified from the available Shadbala data."],
        },
        {
            "title": "Active Yogas And Doshas",
            "items": [
                f"{yoga['name']} ({yoga['type']}) - strength {yoga['strength']}"
                for yoga in chart["active_yogas"]
            ] or ["No active yoga or dosha was reported by the chart service."],
        },
    ]


@router.post("/consult")
async def consult(request: ConsultRequest):
    gemstones = load_gemstones()
    try:
        api_payload = request.model_dump(exclude={"name"})
        api_response = await asyncio.wait_for(calculate_vedic_chart(api_payload), timeout=20)
        chart = parse_chart(api_response)
    except HTTPException:
        raise
    except (httpx.HTTPError, asyncio.TimeoutError):
        logging.exception("consult chart service error")
        raise HTTPException(status_code=503, detail="Chart calculation service unavailable. Please try again.")

    weak_planets = chart["weak_planets"] or ["Jupiter", "Moon"]
    weak_data = {planet: gemstones[planet] for planet in weak_planets if planet in gemstones}

    try:
        full_reading = await asyncio.wait_for(generate_reading(request.name, chart, weak_data), timeout=10)
    except Exception:
        logging.exception("consult ai service error")
        raise HTTPException(status_code=503, detail="AI reading service unavailable. Please try again.")

    recommended = []
    for planet in list(weak_data.keys())[:3]:
        gem = weak_data[planet]
        position = next((p for p in chart["planets"] if p["name"] == planet), {})
        recommended.append(
            {
                "planet": planet,
                "primary_gem": gem["primary"],
                "substitute_gem": gem["substitute"],
                "sanskrit_name": gem["sanskrit"],
                "metal": gem["metal"],
                "finger": gem["finger"],
                "day": gem["day"],
                "min_carat": gem["min_carat"],
                "gem_color": gem["color"],
                "buy_url": gem.get("buy_url", ""),
                "reason_short": f"{gem['primary']} is recommended first to strengthen {planet}. In this chart {planet} is placed in {position.get('sign', 'an unreported sign')} house {position.get('house', 'not reported')} with Shadbala {chart['shadbala'].get(planet, 1.0)}.",
                "planet_position": {
                    "sign": position.get("sign", ""),
                    "house": position.get("house", ""),
                    "nakshatra": position.get("nakshatra", ""),
                    "shadbala_ratio": chart["shadbala"].get(planet, 1.0),
                },
            }
        )

    avoid = [
        {
            "planet": planet,
            "gem_name": gemstones[planet]["primary"],
            "reason": f"{planet} appears strong by Shadbala and should not be amplified without expert review.",
        }
        for planet in chart["strong_planets"]
        if planet in gemstones
    ]

    return {
        "name": request.name,
        "lagna": chart["lagna"],
        "mahadasha_lord": chart["mahadasha_lord"],
        "sade_sati": chart["sade_sati"],
        "recommended_gems": recommended,
        "gems_to_avoid": avoid,
        "analysis_sections": build_analysis_sections(chart),
        "full_reading": full_reading,
        "active_yogas": chart["active_yogas"],
        "chart_planets": chart["planets"],
    }
