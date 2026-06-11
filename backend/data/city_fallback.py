FALLBACK_CITIES = [
    {
        "city_name": "Ambala City",
        "state": "Haryana",
        "country": "India",
        "lat": 30.3782,
        "lng": 76.7767,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Ambala Cantonment",
        "state": "Haryana",
        "country": "India",
        "lat": 30.3398,
        "lng": 76.8200,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Delhi",
        "state": "Delhi",
        "country": "India",
        "lat": 28.6139,
        "lng": 77.2090,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "lat": 19.0760,
        "lng": 72.8777,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "lat": 12.9716,
        "lng": 77.5946,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Chandigarh",
        "state": "Chandigarh",
        "country": "India",
        "lat": 30.7333,
        "lng": 76.7794,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Jaipur",
        "state": "Rajasthan",
        "country": "India",
        "lat": 26.9124,
        "lng": 75.7873,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Amritsar",
        "state": "Punjab",
        "country": "India",
        "lat": 31.6340,
        "lng": 74.8723,
        "tz_str": "Asia/Kolkata",
    },
    {
        "city_name": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "lat": 23.0225,
        "lng": 72.5714,
        "tz_str": "Asia/Kolkata",
    },
]


def fallback_geo_search(query: str) -> list[dict]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    return [
        city
        for city in FALLBACK_CITIES
        if normalized in city["city_name"].lower()
        or normalized in city["state"].lower()
        or normalized in city["country"].lower()
    ][:8]
