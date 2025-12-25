
import zoneinfo
from datetime import datetime
from fastapi import APIRouter
from resources import country_timezones

router = APIRouter()

@router.get("/datetime/{iso_code}")
async def get_datetime(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if not timezone_str:
        return {"error": "ISO code not recognized"}
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {
        "current_datetime": datetime.now(tz),
        "iso_code": iso_code,
        "timezone": timezone_str
    }