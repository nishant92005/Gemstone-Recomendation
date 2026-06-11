PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


def dig(data: dict, *keys, default=None):
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int) and len(current) > key:
            current = current[key]
        else:
            return default
    return default if current is None else current


def _as_planet_list(raw_planets) -> list[dict]:
    if isinstance(raw_planets, dict):
        values = []
        for name, value in raw_planets.items():
            if isinstance(value, dict):
                values.append({"name": value.get("name", name), **value})
        return values
    return raw_planets if isinstance(raw_planets, list) else []


def parse_chart(api_response: dict) -> dict:
    data = api_response.get("data", api_response)
    chart = data.get("chart", data)
    ascendant = dig(chart, "ascendant", default={})
    nakshatra = ascendant.get("nakshatra", {}) if isinstance(ascendant, dict) else {}
    planets = _as_planet_list(dig(chart, "planets", default=dig(data, "planets", default=[])))
    shadbala = dig(chart, "shadbala", default=dig(data, "shadbala", default={}))
    active_periods = dig(data, "vimshottari_dasha", "active_periods", default=[])
    sade_sati = bool(dig(chart, "sade_sati", "active", default=dig(data, "sade_sati", "active", default=False)))
    active_yogas = [
        yoga
        for yoga in dig(data, "yogas", "yogas", default=dig(chart, "yogas", "yogas", default=[]))
        if isinstance(yoga, dict) and yoga.get("active") is True
    ]

    ratios = {}
    for planet in PLANETS:
        entry = shadbala.get(planet, {}) if isinstance(shadbala, dict) else {}
        ratio = entry.get("ratio") if isinstance(entry, dict) else entry
        try:
            ratios[planet] = float(ratio)
        except (TypeError, ValueError):
            ratios[planet] = 1.0

    mahadasha_lord = dig(active_periods, 0, "lord", default="")
    weak = set()
    for planet, ratio in ratios.items():
        if ratio < 1.0:
            weak.add(planet)
    if mahadasha_lord in PLANETS:
        weak.add(mahadasha_lord)
    if sade_sati:
        weak.add("Saturn")
    for yoga in active_yogas:
        if str(yoga.get("type", "")).lower() == "dosha":
            involved = yoga.get("planets") or yoga.get("involves") or []
            if isinstance(involved, str):
                involved = [involved]
            weak.update(planet for planet in involved if planet in PLANETS)

    strong = [planet for planet, ratio in ratios.items() if ratio > 1.3 and planet not in weak]

    formatted_planets = []
    for planet in planets:
        name = planet.get("name") or planet.get("planet")
        if name not in PLANETS:
            continue
        formatted_planets.append(
            {
                "name": name,
                "sign": planet.get("sign", ""),
                "house": planet.get("house", ""),
                "nakshatra": dig(planet, "nakshatra", "name", default=planet.get("nakshatra", "")),
                "nakshatra_lord": dig(planet, "nakshatra", "lord", default=planet.get("nakshatra_lord", "")),
                "is_retrograde": bool(planet.get("is_retrograde", planet.get("retrograde", False))),
                "shadbala_ratio": ratios.get(name, 1.0),
            }
        )

    return {
        "lagna": {
            "sign": ascendant.get("sign", "") if isinstance(ascendant, dict) else "",
            "nakshatra": nakshatra.get("name", "") if isinstance(nakshatra, dict) else "",
            "nakshatra_lord": nakshatra.get("lord", "") if isinstance(nakshatra, dict) else "",
        },
        "mahadasha_lord": mahadasha_lord,
        "sade_sati": sade_sati,
        "planets": formatted_planets,
        "shadbala": ratios,
        "weak_planets": list(weak)[:3],
        "strong_planets": strong,
        "active_yogas": [
            {
                "name": yoga.get("name", ""),
                "type": yoga.get("type", ""),
                "strength": yoga.get("strength", ""),
            }
            for yoga in active_yogas
        ],
    }

