import os
import secrets
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, HTTPException, Response
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"

oauth_states: set[str] = set()
sessions: dict[str, dict] = {}

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=False)


def google_config() -> dict[str, str]:
    return {
        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback"),
        "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:5173"),
    }


@router.get("/auth/google/login")
async def google_login():
    config = google_config()
    if not config["client_id"] or not config["client_secret"]:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured.")

    state = secrets.token_urlsafe(32)
    oauth_states.add(state)
    params = urlencode(
        {
            "client_id": config["client_id"],
            "redirect_uri": config["redirect_uri"],
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "select_account",
        }
    )
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{params}")


@router.get("/auth/google/callback")
async def google_callback(code: str, state: str):
    config = google_config()
    if state not in oauth_states:
        raise HTTPException(status_code=400, detail="Invalid OAuth state.")
    oauth_states.discard(state)

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": config["client_id"],
                    "client_secret": config["client_secret"],
                    "redirect_uri": config["redirect_uri"],
                    "grant_type": "authorization_code",
                },
            )
            if token_response.status_code >= 400:
                detail = token_response.json() if token_response.content else {}
                reason = detail.get("error_description") or detail.get("error") or "Google token exchange failed."
                raise HTTPException(
                    status_code=400,
                    detail=f"Google signup failed: {reason}. Check GOOGLE_CLIENT_SECRET and redirect URI.",
                )
            token_payload = token_response.json()

            id_token = token_payload.get("id_token")
            if not id_token:
                raise HTTPException(status_code=400, detail="Google did not return an ID token.")

            profile_response = await client.get(GOOGLE_TOKENINFO_URL, params={"id_token": id_token})
            profile_response.raise_for_status()
            profile = profile_response.json()
    except HTTPException:
        raise
    except httpx.HTTPError as error:
        raise HTTPException(status_code=400, detail=f"Google signup failed: {str(error)}")

    if profile.get("aud") != config["client_id"]:
        raise HTTPException(status_code=400, detail="Google token audience mismatch.")
    if profile.get("email_verified") not in ("true", True):
        raise HTTPException(status_code=400, detail="Google email is not verified.")

    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "email": profile.get("email"),
        "name": profile.get("name") or profile.get("email"),
        "picture": profile.get("picture"),
        "google_sub": profile.get("sub"),
    }

    response = RedirectResponse(f"{config['frontend_url']}/?auth=google")
    response.set_cookie(
        "navaratna_session",
        session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/auth/me")
async def auth_me(navaratna_session: Optional[str] = Cookie(default=None)):
    user = sessions.get(navaratna_session or "")
    return {"authenticated": bool(user), "user": user}


@router.get("/auth/google/config")
async def google_config_status():
    config = google_config()
    return {
        "client_id_configured": bool(config["client_id"]),
        "client_secret_configured": bool(config["client_secret"]),
        "client_secret_placeholder": config["client_secret"] == "replace_with_rotated_google_client_secret",
        "redirect_uri": config["redirect_uri"],
        "frontend_url": config["frontend_url"],
    }


@router.post("/auth/logout")
async def auth_logout(response: Response, navaratna_session: Optional[str] = Cookie(default=None)):
    if navaratna_session:
        sessions.pop(navaratna_session, None)
    response.delete_cookie("navaratna_session")
    return {"ok": True}
