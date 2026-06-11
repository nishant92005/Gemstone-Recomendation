import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import AsyncGroq, BadRequestError

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=False)

SYSTEM_PROMPT = (
    "You are Jyotish-AI, an expert in classical Vedic astrology and Navaratna gemstone therapy. "
    "You have mastered the Brihat Parashara Hora Shastra, Saravali, and Phaladeepika. You give "
    "warm, precise, personalized gemstone recommendations grounded in the birth chart data provided. "
    "Always explain why a gemstone is recommended by citing specific planetary positions and Shadbala "
    "strength values. Structure your response with clear labeled sections. Speak as a wise, respectful Jyotish advisor."
)

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
FALLBACK_GROQ_MODEL = "llama-3.1-8b-instant"


def build_prompt(name: str, chart: dict, gemstone_data: dict) -> str:
    planet_lines = "\n".join(
        f"- {p['name']}: {p['sign']} house {p['house']}, nakshatra {p['nakshatra']}, retrograde {p['is_retrograde']}"
        for p in chart["planets"]
    )
    strength_lines = "\n".join(
        f"- {planet}: {ratio} ({'weak' if planet in chart['weak_planets'] else 'strong' if planet in chart['strong_planets'] else 'balanced'})"
        for planet, ratio in chart["shadbala"].items()
    )
    yoga_lines = "\n".join(
        f"- {yoga['name']} | {yoga['type']} | {yoga['strength']}" for yoga in chart["active_yogas"]
    ) or "- None reported"

    return f"""Analyze this Vedic birth chart for {name}.

IMPORTANT OUTPUT ORDER
Start with a section titled TOP GEMSTONE RECOMMENDATIONS. Put the gemstones first, before any general analysis.
Then write CHART ANALYSIS, GEMS TO AVOID, OVERALL READING, and BLESSING.

CHART DATA
Lagna: {chart['lagna']['sign']}
Lagna Nakshatra: {chart['lagna']['nakshatra']} (Lord: {chart['lagna']['nakshatra_lord']})
Current Mahadasha: {chart['mahadasha_lord']}
Sade Sati Active: {chart['sade_sati']}

PLANETARY POSITIONS
{planet_lines}

PLANETARY STRENGTH
{strength_lines}

IDENTIFIED WEAK PLANETS
{', '.join(chart['weak_planets'])}

ACTIVE YOGAS AND DOSHAS
{yoga_lines}

GEMSTONE KNOWLEDGE BASE
{json.dumps(gemstone_data, ensure_ascii=False)}

TASK
First, recommend 2 to 3 primary gemstones at the very top. For each, state which planet it strengthens and why that planet matters for this chart, name the primary gem and substitute, give wearing details, brief puja instructions, and a personalized reason citing house and nakshatra. Second, write the chart analysis. Third, list gemstones to avoid. Fourth, write one overall reading paragraph. Fifth, end with one Sanskrit blessing in transliterated Roman script followed by English translation."""


async def generate_reading(name: str, chart: dict, gemstone_data: dict) -> str:
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key":
        raise RuntimeError("GROQ_API_KEY is not configured.")

    client = AsyncGroq(api_key=api_key)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_prompt(name, chart, gemstone_data)},
    ]
    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL

    try:
        completion = await client.chat.completions.create(
            model=model,
            temperature=0.72,
            max_tokens=1500,
            messages=messages,
        )
    except BadRequestError as error:
        message = str(error).lower()
        if "decommissioned" not in message and "model" not in message:
            raise
        completion = await client.chat.completions.create(
            model=FALLBACK_GROQ_MODEL,
            temperature=0.72,
            max_tokens=1500,
            messages=messages,
        )
    return completion.choices[0].message.content or ""
