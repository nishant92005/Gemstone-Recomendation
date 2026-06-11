# Navaratna

Responsive React + FastAPI app scaffold for the AI Vedic gemstone recommendation app.

## Project Notes

### Tech Stack

- Frontend: React, Vite, React Router, Axios, custom CSS, Three.js-ready visual structure.
- Backend: FastAPI, Pydantic, httpx, python-dotenv, Groq SDK.
- External services: FreeAstroAPI for Vedic chart data, Groq for AI-generated analysis, Google OAuth for signup.

### Architecture

- `frontend/` contains the single-page React app with routed pages for home, consultation, app info, and developer info.
- `backend/` exposes API routes for health, geo search, consultation, and Google authentication.
- `backend/services/` contains integrations and parsing logic for astrology data and AI reading generation.
- `backend/data/` stores gemstone knowledge and fallback city data.
- The consult flow is: user birth details -> geo lookup -> FreeAstroAPI chart -> chart parser -> gemstone mapping -> Groq reading -> structured frontend result.

### Assumptions

- API keys are provided locally through `.env` and are not committed.
- FreeAstroAPI responses may vary, so chart parsing uses defensive fallbacks.
- Fallback city search is available for development when FreeAstroAPI geo search is unavailable.
- Gemstone recommendations are for spiritual/self-reflection purposes and should not replace certified Jyotish advice.

### Future Improvements

- Store user sessions and readings in a database instead of in-memory dictionaries.
- Add persistent auth/session management with secure production cookie settings.
- Improve FreeAstroAPI response normalization with real sample fixtures and tests.
- Add richer product mapping for every primary and substitute gemstone.
- Add Playwright visual tests for mobile, tablet, and desktop layouts.
- Deploy frontend/backend with production CORS, HTTPS, and environment-specific config.

## Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Alternative from the project root:

```powershell
backend\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload
```

API keys live in the project root `.env`.

Google signup also reads these values from `.env`:

```powershell
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

Groq uses `llama-3.3-70b-versatile` by default. You can override it with:

```powershell
GROQ_MODEL=llama-3.3-70b-versatile
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend shell is responsive for mobile, tablet, and desktop breakpoints.

Optional frontend env:

```powershell
$env:VITE_API_BASE_URL="http://localhost:8000"
```
