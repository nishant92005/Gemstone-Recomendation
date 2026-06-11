from fastapi import APIRouter, Query

try:
    from backend.services.astro import search_geo
except ModuleNotFoundError:
    from services.astro import search_geo

router = APIRouter(prefix="/api", tags=["geo"])
cache: dict[str, list[dict]] = {}


@router.get("/geo-search")
async def geo_search(q: str = Query(..., min_length=2)):
    key = q.strip().lower()
    if key in cache:
        return cache[key]
    results = await search_geo(key)
    cache[key] = results
    return results
