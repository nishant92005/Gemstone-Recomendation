import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, NavLink, Route, Routes, useLocation } from "react-router-dom";
import axios from "axios";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const planets = [
  ["Sun", "सूर्य", "Ruby", "#C0392B"],
  ["Moon", "चन्द्र", "Pearl", "#F5ECD7"],
  ["Mars", "मंगल", "Red Coral", "#E74C3C"],
  ["Mercury", "बुध", "Emerald", "#00BF72"],
  ["Jupiter", "गुरु", "Yellow Sapphire", "#FFB830"],
  ["Venus", "शुक्र", "Diamond", "#FF4FA3"],
  ["Saturn", "शनि", "Blue Sapphire", "#1A6BFF"],
  ["Rahu", "राहु", "Hessonite", "#7B2FBE"],
  ["Ketu", "केतु", "Cat's Eye", "#8B7355"],
];

function Mandala({ mini = false }) {
  return (
    <div className={mini ? "mandala mini-mandala" : "mandala"} aria-hidden="true">
      {planets.map(([name, , , color], index) => (
        <span key={name} style={{ "--i": index, "--gem": color }} />
      ))}
    </div>
  );
}

function Particles() {
  return (
    <>
      <div className="cosmic-bg" aria-hidden="true">
        <span className="aurora aurora-one" />
        <span className="aurora aurora-two" />
        <span className="aurora aurora-three" />
        <span className="orbit-ring orbit-ring-one" />
        <span className="orbit-ring orbit-ring-two" />
        <span className="yantra yantra-one" />
        <span className="yantra yantra-two" />
        <span className="energy-wave energy-wave-one" />
        <span className="energy-wave energy-wave-two" />
      </div>
      <div className="particles" aria-hidden="true">
        {Array.from({ length: 64 }).map((_, index) => (
          <i key={index} style={{ "--i": index }} />
        ))}
      </div>
      <div className="shooting-stars" aria-hidden="true">
        {Array.from({ length: 7 }).map((_, index) => (
          <span key={index} style={{ "--i": index }} />
        ))}
      </div>
    </>
  );
}

function CustomCursor() {
  const [point, setPoint] = useState({ x: -100, y: -100 });
  useEffect(() => {
    const move = (event) => setPoint({ x: event.clientX, y: event.clientY });
    window.addEventListener("pointermove", move);
    return () => window.removeEventListener("pointermove", move);
  }, []);

  return (
    <>
      <div className="cursor-dot" style={{ left: point.x, top: point.y }}>ॐ</div>
      <div className="cursor-ring" style={{ left: point.x, top: point.y }} />
    </>
  );
}

function PageTransition() {
  const location = useLocation();
  const [active, setActive] = useState(false);

  useEffect(() => {
    setActive(true);
    const id = setTimeout(() => setActive(false), 700);
    return () => clearTimeout(id);
  }, [location.pathname]);

  return <div className={active ? "om-transition active" : "om-transition"}>ॐ</div>;
}

function Navbar() {
  const [open, setOpen] = useState(false);
  const [auth, setAuth] = useState({ authenticated: false, user: null });

  useEffect(() => {
    axios.get(`${API_BASE}/auth/me`, { withCredentials: true })
      .then((response) => setAuth(response.data))
      .catch(() => setAuth({ authenticated: false, user: null }));
  }, []);

  const login = () => {
    window.location.href = `${API_BASE}/auth/google/login`;
  };

  const logout = async () => {
    await axios.post(`${API_BASE}/auth/logout`, {}, { withCredentials: true });
    setAuth({ authenticated: false, user: null });
  };

  return (
    <header className="navbar">
      <NavLink className="brand" to="/" onClick={() => setOpen(false)}>
        <span>ॐ</span> NAVARATNA
      </NavLink>
      <button className="menu-button" type="button" aria-label="Toggle menu" onClick={() => setOpen(!open)}>
        <span />
        <span />
        <span />
      </button>
      <nav className={open ? "nav-links open" : "nav-links"}>
        <NavLink to="/" onClick={() => setOpen(false)}>Home</NavLink>
        <NavLink to="/consult" onClick={() => setOpen(false)}>Consult</NavLink>
        <NavLink to="/about-app" onClick={() => setOpen(false)}>About</NavLink>
        <NavLink to="/about-dev" onClick={() => setOpen(false)}>Developer</NavLink>
        {auth.authenticated ? (
          <button className="auth-chip" type="button" onClick={logout}>
            {auth.user?.picture && <img src={auth.user.picture} alt="" />}
            <span>{auth.user?.name || "Signed in"}</span>
          </button>
        ) : (
          <button className="google-button" type="button" onClick={login}>
            <span>G</span> Sign up
          </button>
        )}
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-om">ॐ</div>
      <div className="footer-grid">
        <div>
          <h2>NAVARATNA</h2>
          <p>AI-guided gemstone readings inspired by Jyotish tradition.</p>
        </div>
        <div>
          <a href="/">Home</a>
          <a href="/consult">Consult</a>
          <p className="devanagari">सर्वे भवन्तु सुखिनः</p>
          <p>May all beings be happy.</p>
        </div>
        <div>
          <p>Built with React, FastAPI, Python, Groq AI, and cosmic patience.</p>
        </div>
      </div>
    </footer>
  );
}

function Layout() {
  return (
    <>
      <Particles />
      <CustomCursor />
      <Navbar />
      <PageTransition />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/consult" element={<ConsultPage />} />
        <Route path="/about-app" element={<AboutAppPage />} />
        <Route path="/about-dev" element={<AboutDeveloperPage />} />
      </Routes>
      <Mandala mini />
      <Footer />
    </>
  );
}

function HomePage() {
  return (
    <main>
      <section className="hero">
        <Mandala />
        <div className="hero-content reveal">
          <p className="eyebrow">* VEDIC AI WISDOM *</p>
          <h1>NAVARATNA</h1>
          <p className="devanagari hero-script">नवरत्न</p>
          <p className="tagline">Where the stars speak, and the stones listen.</p>
          <a className="cta" href="/consult">Reveal My Gemstones</a>
          <a className="under-link" href="#journey">Learn how it works ↓</a>
        </div>
      </section>

      <Section title="What Is Navaratna">
        <div className="card-grid three">
          <InfoCard icon="ॐ" title="Ancient Wisdom" text="Vedic astrology studies the Navagraha, the nine planetary forces shaping temperament and timing." />
          <InfoCard icon="✺" title="AI Analysis" text="Birth chart data, Shadbala ratios, and dasha context are interpreted into a focused reading." />
          <InfoCard icon="◆" title="Sacred Remedies" text="Gem recommendations translate planetary imbalance into practical ritual guidance." />
        </div>
      </Section>

      <Section id="journey" title="The Cosmic Journey">
        <div className="timeline">
          {["Enter Birth Details", "Chart Calculated", "AI Interprets", "Gemstones Revealed"].map((step, index) => (
            <article className="step-card" key={step}>
              <span>{["१", "२", "३", "४"][index]}</span>
              <h3>{step}</h3>
              <p>{["Share name, date, time, and birthplace.", "FreeAstroAPI calculates the Vedic chart.", "Groq explains chart strengths and remedies.", "Receive sacred gems and wearing details."][index]}</p>
            </article>
          ))}
        </div>
      </Section>

      <Section title="Navagraha - The Nine Cosmic Rulers" subtitle="नवग्रह">
        <div className="planet-grid">
          {planets.map(([name, sanskrit, gem, color]) => (
            <article className="planet-card" key={name} style={{ "--planet": color }}>
              <div className="planet-top">
                <div className="orbit"><span /></div>
                <div className="stone-orb" aria-hidden="true">
                  <span />
                  <i />
                </div>
              </div>
              <div className="planet-copy">
                <h3>{name}</h3>
                <p className="devanagari">{sanskrit}</p>
                <strong>{gem}</strong>
              </div>
            </article>
          ))}
        </div>
      </Section>

      <Section title="Trusted By Seekers">
        <div className="stats">
          <Stat value="12,000+" label="Charts Analyzed" />
          <Stat value="9" label="Sacred Gems" />
          <Stat value="100%" label="Vedic Accuracy" />
        </div>
        <div className="card-grid three">
          <InfoCard title="A luminous guide" text="The reading felt thoughtful, specific, and beautifully presented." />
          <InfoCard title="Clear remedies" text="I loved seeing the ritual details alongside the gemstone suggestion." />
          <InfoCard title="Modern and sacred" text="Ancient symbolism with a polished AI experience." />
        </div>
      </Section>

      <section className="final-cta">
        <h2>Your Stars Have Something To Say</h2>
        <p>Get your personalized Vedic gemstone reading in under 60 seconds.</p>
        <a className="cta" href="/consult">Reveal My Gemstones</a>
      </section>
    </main>
  );
}

function Section({ id, title, subtitle, children }) {
  return (
    <section className="section reveal" id={id}>
      <div className="section-title">
        <h2>{title}</h2>
        {subtitle && <p className="devanagari">{subtitle}</p>}
      </div>
      {children}
    </section>
  );
}

function InfoCard({ icon, title, text }) {
  return (
    <article className="card">
      {icon && <div className="card-icon">{icon}</div>}
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

function Stat({ value, label }) {
  return (
    <article className="stat">
      <strong>{value}</strong>
      <span>{label}</span>
    </article>
  );
}

function ConsultPage() {
  const [state, setState] = useState("form");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState(null);
  const [unknownTime, setUnknownTime] = useState(false);
  const [form, setForm] = useState({
    name: "",
    birthDate: "",
    birthTime: "12:00",
    city: "",
  });

  useEffect(() => {
    if (form.city.trim().length < 2 || selectedCity?.label === form.city) {
      setCities([]);
      return;
    }

    const id = setTimeout(async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/geo-search`, { params: { q: form.city } });
        setCities(response.data);
      } catch {
        setCities([]);
      }
    }, 350);

    return () => clearTimeout(id);
  }, [form.city, selectedCity]);

  const submit = async (event) => {
    event.preventDefault();
    setError("");

    let cityForReading = selectedCity;
    if (!cityForReading) {
      try {
        const response = await axios.get(`${API_BASE}/api/geo-search`, { params: { q: form.city } });
        cityForReading = response.data?.[0];
      } catch {
        cityForReading = null;
      }
    }

    if (!cityForReading) {
      setError("Please select a city from the suggestions.");
      return;
    }

    const [year, month, day] = form.birthDate.split("-").map(Number);
    const [hour, minute] = (unknownTime ? "12:00" : form.birthTime).split(":").map(Number);
    setState("loading");

    try {
      const response = await axios.post(`${API_BASE}/api/consult`, {
        name: form.name,
        year,
        month,
        day,
        hour,
        minute,
        lat: Number(cityForReading.lat),
        lng: Number(cityForReading.lng),
        tz_str: cityForReading.tz_str || "Asia/Kolkata",
      });
      setResult(response.data);
      setState("results");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "The reading could not be completed.");
      setState("form");
    }
  };

  if (state === "loading") return <LoadingState />;
  if (state === "results" && result) return <Results result={result} onReset={() => setState("form")} />;

  return (
    <main className="consult-page page-pad">
      <div className="orrery" aria-hidden="true">
        <Mandala />
        <p className="devanagari">नवग्रह</p>
      </div>
      <form className="consult-form card" onSubmit={submit}>
        <h1>Enter Your Birth Details</h1>
        <p className="devanagari">जन्म विवरण</p>
        <label>
          Your Name
          <span className="devanagari">आपका नाम</span>
          <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        </label>
        <label>
          Date of Birth
          <input required type="date" value={form.birthDate} onChange={(e) => setForm({ ...form, birthDate: e.target.value })} />
        </label>
        <label>
          Time of Birth
          <input required type="time" disabled={unknownTime} value={form.birthTime} onChange={(e) => setForm({ ...form, birthTime: e.target.value })} />
        </label>
        <label className="toggle">
          <input type="checkbox" checked={unknownTime} onChange={(e) => setUnknownTime(e.target.checked)} />
          I do not know my exact time
        </label>
        {unknownTime && <p className="hint">Approximate time may affect accuracy. Noon will be used.</p>}
        <label className="city-field">
          City of Birth
          <input required value={form.city} onChange={(e) => { setSelectedCity(null); setForm({ ...form, city: e.target.value }); }} />
          {cities.length > 0 && (
            <div className="city-menu">
              {cities.map((city) => {
                const label = `${city.city_name}, ${city.state || city.country}`;
                return (
                  <button type="button" key={`${label}-${city.lat}`} onClick={() => { setSelectedCity({ ...city, label }); setForm({ ...form, city: label }); setCities([]); }}>
                    {label}
                  </button>
                );
              })}
            </div>
          )}
        </label>
        {error && <p className="error">{error}</p>}
        <button className="cta full" type="submit">Read The Stars</button>
        <p className="hint">Your birth data is never stored. Analysis happens in real time.</p>
      </form>
    </main>
  );
}

function LoadingState() {
  return (
    <main className="loading-state">
      <div className="chakra">✺</div>
      {["Calculating planetary positions", "Reading your Navagraha chart", "Consulting the ancient Shastra", "Preparing your sacred recommendations"].map((line) => (
        <p key={line}><span />{line}</p>
      ))}
      <div className="progress" />
      <small className="devanagari">ग्रहाणां चरितं दिव्यं</small>
    </main>
  );
}

function Results({ result, onReset }) {
  const share = async () => {
    await navigator.clipboard?.writeText(result.full_reading);
    alert("Reading copied to clipboard.");
  };

  return (
    <main className="results page-pad">
      <Section title="Your Sacred Gemstones" subtitle="Recommended first, based on your FreeAstroAPI chart and AI reading">
        <div className="gem-grid">
          {result.recommended_gems.map((gem) => <GemCard key={gem.planet} gem={gem} />)}
        </div>
      </Section>
      <section className="card summary-card">
        <h1>{result.name}'s Vedic Birth Chart</h1>
        <div className="badges">
          <span>Lagna: {result.lagna.sign || "Unknown"}</span>
          <span>Nakshatra: {result.lagna.nakshatra || "Unknown"}</span>
          <span>Mahadasha: {result.mahadasha_lord || "Unknown"}</span>
        </div>
      </section>
      <Kundli planets={result.chart_planets} />
      <AnalysisSections sections={result.analysis_sections || []} />
      <section className="card avoid">
        <h2>Gems To Avoid For Now</h2>
        {(result.gems_to_avoid.length ? result.gems_to_avoid : [{ planet: "None", gem_name: "No avoid list", reason: "No strongly amplified planets were identified." }]).map((item) => (
          <article className="avoid-item" key={item.planet}>
            <strong>{item.gem_name}</strong>
            <span>{item.reason}</span>
          </article>
        ))}
      </section>
      <details className="card reading">
        <summary>Your Complete Cosmic Reading</summary>
        <StructuredReading text={result.full_reading} />
      </details>
      <div className="actions">
        <button className="cta" type="button" onClick={onReset}>Get Another Reading</button>
        <button className="cta ghost" type="button" onClick={share}>Share My Reading</button>
      </div>
    </main>
  );
}

function AnalysisSections({ sections }) {
  if (!sections.length) return null;

  return (
    <section className="analysis-grid">
      {sections.map((section) => (
        <article className="analysis-card card" key={section.title}>
          <h3>{section.title}</h3>
          <ul>
            {section.items.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </article>
      ))}
    </section>
  );
}

function StructuredReading({ text }) {
  const cleanLine = (line) => line
    .replace(/^#{1,6}\s*/, "")
    .replace(/^[-*•\d.]+\s*/, "")
    .replace(/\*\*/g, "")
    .replace(/^\*+\s*/, "")
    .replace(/\s*\*+$/g, "")
    .trim();

  const blocks = text
    .replace(/\*\*/g, "")
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .filter(Boolean);

  return (
    <div className="structured-reading">
      {blocks.map((block, index) => {
        const cleanedBlock = cleanLine(block);
        const isHeading = /^#{1,6}\s/.test(block)
          || /^[A-Z][A-Z\s]+:?$/.test(cleanedBlock)
          || cleanedBlock.toUpperCase().includes("RECOMMENDATIONS")
          || cleanedBlock.toUpperCase().includes("CHART ANALYSIS")
          || cleanedBlock.toUpperCase().includes("GEMS TO AVOID")
          || cleanedBlock.toUpperCase().includes("BLESSING");

        if (isHeading) return <h3 key={index}>{cleanedBlock.replace(/:$/, "")}</h3>;

        const lines = block.split("\n").map(cleanLine).filter(Boolean);
        if (lines.length > 1) {
          return (
            <ul key={index}>
              {lines.map((line) => <li key={line}>{line}</li>)}
            </ul>
          );
        }

        return <p key={index}>{cleanedBlock}</p>;
      })}
    </div>
  );
}

function Kundli({ planets: chartPlanets }) {
  const labels = useMemo(() => chartPlanets?.slice(0, 12) || [], [chartPlanets]);

  return (
    <section className="kundli" aria-label="Decorative kundli chart">
      {Array.from({ length: 12 }).map((_, index) => (
        <div key={index}>{labels[index]?.name?.slice(0, 2) || index + 1}</div>
      ))}
    </section>
  );
}

function GemCard({ gem }) {
  return (
    <article className="gem-card card" style={{ "--gem": gem.gem_color }}>
      <div className="gem-stage" aria-hidden="true">
        <div className="gem-shape">
          <span />
          <i />
        </div>
      </div>
      <div>
        <h3>{gem.primary_gem}</h3>
        <p className="devanagari">{gem.sanskrit_name}</p>
        <span className="badge">{gem.planet}</span>
        {gem.planet_position && (
          <div className="position-strip">
            <span>House {gem.planet_position.house || "?"}</span>
            <span>{gem.planet_position.sign || "Sign ?"}</span>
            <span>Shadbala {gem.planet_position.shadbala_ratio}</span>
          </div>
        )}
        <div className="details-grid">
          <span>{gem.min_carat} ct</span>
          <span>{gem.finger}</span>
          <span>{gem.metal}</span>
          <span>{gem.day}</span>
        </div>
        <details>
          <summary>Wearing Ritual</summary>
          <p>Cleanse the gem, offer a quiet prayer, and wear it at sunrise on {gem.day}.</p>
        </details>
        <p><em>{gem.reason_short}</em></p>
        <small>Alternative: {gem.substitute_gem}</small>
        {gem.buy_url && (
          <a className="buy-link" href={gem.buy_url} target="_blank" rel="noreferrer">
            Buy {gem.primary_gem}
          </a>
        )}
      </div>
    </article>
  );
}

function AboutAppPage() {
  return (
    <main className="page-pad">
      <section className="sub-hero"><Mandala /><h1>The Science Of Sacred Stones</h1></section>
      <Section title="What Is Vedic Gemology">
        <div className="split">
          <div className="gem-cluster">
            {planets.map(([name, , , color]) => <span key={name} style={{ background: color }} />)}
          </div>
          <div className="card">
            <p>Jyotish reads planetary patterns as symbolic guidance. Navaratna tradition connects the nine cosmic rulers with gemstones used for reflection, ritual, and spiritual alignment.</p>
            <blockquote>As above, so below - the cosmos writes itself in stone.</blockquote>
          </div>
        </div>
      </Section>
      <Section title="The Nine Gems And Their Planets">
        <div className="gem-table">
          {planets.map(([name, sanskrit, gem, color]) => (
            <div key={name} style={{ "--planet": color }}>
              <strong>{name}</strong>
              <span>{gem}</span>
              <span className="devanagari">{sanskrit}</span>
              <span>Ritual day varies by planet</span>
            </div>
          ))}
        </div>
      </Section>
      <Section title="How The AI Works">
        <div className="card-grid three">
          <InfoCard title="FreeAstroAPI" text="Calculates Lahiri ayanamsha chart data." />
          <InfoCard title="Shadbala" text="Ratios identify weak and strong planets." />
          <InfoCard title="Groq LLM" text="Turns chart context into a personal explanation." />
        </div>
      </Section>
      <section className="card scroll-card">Navaratna is a tool for spiritual exploration and self-reflection. Always consult a certified Jyotish practitioner for life decisions.</section>
    </main>
  );
}

function AboutDeveloperPage() {
  return (
    <main className="page-pad developer-page">
      <section className="sub-hero"><Mandala /><h1>The Mind Behind The Cosmos</h1></section>
      <section className="developer-card card">
        <div className="avatar">
          <img src="/images/nishant.jpeg" alt="Nishant" />
        </div>
        <h2>Nishant</h2>
        <p>Full-Stack Developer and AI Builder</p>
        <p>Passionate about building meaningful products at the intersection of ancient wisdom and modern technology.</p>
        <div className="chips">{["React", "FastAPI", "Python", "Groq AI", "Three.js", "Vedic Astrology"].map((chip) => <span key={chip}>{chip}</span>)}</div>
        <div className="socials">
          <a href="https://github.com/nishant92005" target="_blank" rel="noreferrer">GitHub</a>
          <a href="https://www.linkedin.com/in/nishant-sh4rma/" target="_blank" rel="noreferrer">LinkedIn</a>
        </div>
      </section>
      <Section title="Other Projects">
        <div className="card-grid three">
          <InfoCard title="PotionCheck" text="AI-powered food ingredient safety app." />
          <InfoCard title="Cosmic Tools" text="Experimental astrology utilities." />
          <InfoCard title="AI Studio" text="Practical products with thoughtful interfaces." />
        </div>
      </Section>
      <section className="quote-card card">I build at the intersection of ancient wisdom and modern AI because the best technology amplifies human intuition.</section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Layout />
  </BrowserRouter>
);
