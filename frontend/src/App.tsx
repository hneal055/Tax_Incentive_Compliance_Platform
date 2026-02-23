import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { LayoutDashboard, Film, Calculator, Globe, Bot, Settings, Bell, RefreshCw, Plus, ChevronRight, AlertCircle, TrendingUp, Briefcase, DollarSign, Search, Filter } from "lucide-react";

const COLORS = {
  bg: "#0d1117",
  sidebar: "#161b27",
  sidebarBorder: "#1e2535",
  card: "#ffffff",
  cardBorder: "#e5e9f0",
  accent: "#0ea5e9",
  accentDark: "#0284c7",
  accentGlow: "rgba(14,165,233,0.15)",
  success: "#10b981",
  warning: "#f59e0b",
  danger: "#ef4444",
  purple: "#8b5cf6",
  text: "#0f172a",
  textMuted: "#64748b",
  textLight: "#94a3b8",
  mainBg: "#f1f5f9",
};

const budgetData = [
  { name: "The Silent Hori...", budget: 15000000, actual: 9200000 },
  { name: "Echoes of Midni...", budget: 8000000, actual: 0 },
  { name: "Neon Pulse", budget: 500000, actual: 480000 },
];

const productions = [
  { id: 1, title: "The Silent Horizon", type: "Feature Film", status: "PRODUCTION", statusColor: "#0ea5e9", budget: "$15.0M", location: "Georgia" },
  { id: 2, title: "Echoes of Midnight", type: "Television Series", status: "DEVELOPMENT", statusColor: "#8b5cf6", budget: "$8.0M", location: "United Kingdom" },
  { id: 3, title: "Neon Pulse", type: "Commercial", status: "RELEASED", statusColor: "#10b981", budget: "$0.5M", location: "New York" },
];

const jurisdictions = [
  { code: "US", state: "Georgia", base: "20% BASE", agency: "Georgia Department of Eco...", minSpend: "$500k" },
  { code: "US", state: "California", base: "25% BASE", agency: "California Film Commission", minSpend: "$1,000k" },
  { code: "US", state: "New York", base: "30% BASE", agency: "Governor's Office of Motio...", minSpend: "$0k" },
  { code: "GB", state: "United Kingdom", base: "25% BASE", agency: "British Film Commission", minSpend: "$0k" },
  { code: "CA", state: "Ontario", base: "35% BASE", agency: "Ontario Creates", minSpend: "$100k" },
];

const regulatoryFeed = [
  { source: "California Film Commission", time: "2h ago", text: "Proposed expansion of the 30-mile studio zone currently under committee review." },
  { source: "British Film Commission", time: "5h ago", text: "New guidance issued for VFX expenditure qualification under updates." },
  { source: "Georgia Dept. of Econ Dev", time: "1d ago", text: "Fiscal year cap status: 65% utilized. Applications open." },
];

export default function PilotForgeDashboard() {
  const [active, setActive] = useState("dashboard");

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "productions", label: "Productions", icon: Film },
    { id: "calculator", label: "Incentive Calculator", icon: Calculator },
    { id: "jurisdictions", label: "Jurisdictions", icon: Globe },
    { id: "advisor", label: "AI Advisor", icon: Bot, badge: "NEW" },
  ];

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "'DM Sans', 'Segoe UI', sans-serif", background: COLORS.mainBg }}>
      {/* Sidebar */}
      <div style={{ width: 220, background: COLORS.sidebar, borderRight: `1px solid ${COLORS.sidebarBorder}`, display: "flex", flexDirection: "column", flexShrink: 0 }}>
        {/* Logo */}
        <div style={{ padding: "20px 16px", display: "flex", alignItems: "center", gap: 10, borderBottom: `1px solid ${COLORS.sidebarBorder}` }}>
          <div style={{ width: 36, height: 36, background: COLORS.accent, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <DollarSign size={20} color="#fff" />
          </div>
          <span style={{ color: "#fff", fontWeight: 700, fontSize: 18, letterSpacing: "-0.3px" }}>PilotForge</span>
        </div>

        {/* Nav */}
        <nav style={{ flex: 1, padding: "12px 8px" }}>
          {navItems.map(({ id, label, icon: Icon, badge }) => {
            const isActive = active === id;
            return (
              <button key={id} onClick={() => setActive(id)} style={{
                width: "100%", display: "flex", alignItems: "center", gap: 10,
                padding: "9px 12px", borderRadius: 8, border: "none", cursor: "pointer",
                background: isActive ? COLORS.accentGlow : "transparent",
                color: isActive ? COLORS.accent : "#94a3b8",
                fontSize: 14, fontWeight: isActive ? 600 : 400,
                marginBottom: 2, textAlign: "left", transition: "all 0.15s",
                borderLeft: isActive ? `3px solid ${COLORS.accent}` : "3px solid transparent",
              }}>
                <Icon size={17} />
                <span style={{ flex: 1 }}>{label}</span>
                {badge && <span style={{ fontSize: 10, background: COLORS.accent, color: "#fff", padding: "2px 6px", borderRadius: 4, fontWeight: 700 }}>{badge}</span>}
              </button>
            );
          })}
        </nav>

        {/* User */}
        <div style={{ padding: "12px 16px", borderTop: `1px solid ${COLORS.sidebarBorder}`, display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#334155", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#94a3b8", fontSize: 13 }}>FM</span>
          </div>
          <div>
            <div style={{ color: "#e2e8f0", fontSize: 13, fontWeight: 600 }}>Finance Manager</div>
            <div style={{ color: "#64748b", fontSize: 11 }}>Pro Account</div>
          </div>
          <Settings size={15} color="#475569" style={{ marginLeft: "auto", cursor: "pointer" }} />
        </div>
      </div>

      {/* Main */}
      <div style={{ flex: 1, overflow: "auto" }}>
        {active === "dashboard" && <DashboardView />}
        {active === "productions" && <ProductionsView />}
        {active === "calculator" && <CalculatorView />}
        {active === "jurisdictions" && <JurisdictionsView />}
        {active === "advisor" && <AdvisorView />}
      </div>
    </div>
  );
}

function MetricCard({ label, value, sub, icon, iconBg }) {
  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: "20px 24px", border: `1px solid ${COLORS.cardBorder}`, display: "flex", alignItems: "center", justifyContent: "space-between", flex: 1 }}>
      <div>
        <div style={{ color: COLORS.textMuted, fontSize: 12, fontWeight: 500, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>{label}</div>
        <div style={{ color: COLORS.text, fontSize: 26, fontWeight: 700, letterSpacing: "-0.5px" }}>{value}</div>
        <div style={{ color: COLORS.textLight, fontSize: 12, marginTop: 4 }}>{sub}</div>
      </div>
      <div style={{ width: 44, height: 44, borderRadius: 10, background: iconBg, display: "flex", alignItems: "center", justifyContent: "center" }}>
        {icon}
      </div>
    </div>
  );
}

function DashboardView() {
  return (
    <div style={{ padding: 32 }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 26, fontWeight: 700, color: COLORS.text, margin: 0, letterSpacing: "-0.5px" }}>Executive Dashboard</h1>
        <p style={{ color: COLORS.textMuted, fontSize: 14, marginTop: 4 }}>Overview of active productions and tax incentive performance.</p>
      </div>

      {/* Metric Cards */}
      <div style={{ display: "flex", gap: 16, marginBottom: 28 }}>
        <MetricCard label="Budget Volume" value="$23.5M" sub="Total planned" iconBg="#dbeafe" icon={<Briefcase size={20} color="#3b82f6" />} />
        <MetricCard label="Est. Tax Credits" value="$3.5M" sub="Avg 25% rate" iconBg="#dcfce7" icon={<TrendingUp size={20} color="#10b981" />} />
        <MetricCard label="Active Projects" value="3" sub="Tracked productions" iconBg="#f3e8ff" icon={<Film size={20} color="#8b5cf6" />} />
        <MetricCard label="Alerts" value="3" sub="Action required" iconBg="#fef3c7" icon={<AlertCircle size={20} color="#f59e0b" />} />
      </div>

      {/* Chart */}
      <div style={{ background: "#fff", borderRadius: 12, padding: 24, border: `1px solid ${COLORS.cardBorder}` }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, color: COLORS.text, marginTop: 0, marginBottom: 20 }}>Budget vs. Actual Spend</h2>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={budgetData} barGap={4}>
            <XAxis dataKey="name" tick={{ fontSize: 12, fill: COLORS.textMuted }} axisLine={false} tickLine={false} />
            <YAxis tickFormatter={v => `$${(v / 1000000).toFixed(0)}M`} tick={{ fontSize: 12, fill: COLORS.textMuted }} axisLine={false} tickLine={false} />
            <Tooltip formatter={(v) => `$${(v / 1000000).toFixed(1)}M`} contentStyle={{ borderRadius: 8, border: "1px solid #e2e8f0", fontSize: 13 }} />
            <Legend wrapperStyle={{ fontSize: 13, paddingTop: 16 }} />
            <Bar dataKey="budget" name="Budget" fill="#38bdf8" radius={[4, 4, 0, 0]} />
            <Bar dataKey="actual" name="Actual" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function ProductionsView() {
  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24 }}>
        <h1 style={{ fontSize: 26, fontWeight: 700, color: COLORS.text, margin: 0, letterSpacing: "-0.5px" }}>Productions</h1>
        <button style={{ display: "flex", alignItems: "center", gap: 8, background: COLORS.accent, color: "#fff", border: "none", borderRadius: 8, padding: "10px 18px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
          <Plus size={16} /> New Production
        </button>
      </div>

      {/* Filters */}
      <div style={{ background: "#fff", borderRadius: 12, padding: "14px 20px", border: `1px solid ${COLORS.cardBorder}`, marginBottom: 20, display: "flex", alignItems: "center", gap: 16 }}>
        <div>
          <div style={{ fontSize: 10, color: COLORS.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Project Status</div>
          <select style={{ border: `1px solid ${COLORS.cardBorder}`, borderRadius: 6, padding: "6px 10px", fontSize: 13, color: COLORS.text, background: "#fff" }}>
            <option>All Statuses</option>
          </select>
        </div>
        <div>
          <div style={{ fontSize: 10, color: COLORS.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Production Type</div>
          <select style={{ border: `1px solid ${COLORS.cardBorder}`, borderRadius: 6, padding: "6px 10px", fontSize: 13, color: COLORS.text, background: "#fff" }}>
            <option>All Types</option>
          </select>
        </div>
        <div style={{ marginLeft: "auto", color: COLORS.textMuted, fontSize: 13 }}>3 Projects Tracked</div>
      </div>

      {/* Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        {productions.map(p => (
          <div key={p.id} style={{ background: "#fff", borderRadius: 12, padding: 24, border: `1px solid ${COLORS.cardBorder}`, cursor: "pointer", transition: "box-shadow 0.15s" }}
            onMouseEnter={e => e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,0.08)"}
            onMouseLeave={e => e.currentTarget.style.boxShadow = "none"}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
              <Film size={18} color={COLORS.textLight} />
              <span style={{ fontSize: 11, fontWeight: 700, color: p.statusColor, letterSpacing: "0.05em" }}>{p.status}</span>
            </div>
            <div style={{ fontSize: 17, fontWeight: 700, color: COLORS.text, marginBottom: 4 }}>{p.title}</div>
            <div style={{ fontSize: 13, color: COLORS.textMuted, marginBottom: 16 }}>{p.type}</div>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 4, color: COLORS.textMuted, fontSize: 13 }}>
                <DollarSign size={13} /> {p.budget}
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 4, color: COLORS.textMuted, fontSize: 13 }}>
                <Globe size={13} /> {p.location}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function CalculatorView() {
  const [result, setResult] = useState(null);
  const [prod, setProd] = useState("The Silent Horizon");
  const [juris, setJuris] = useState("Georgia");

  const run = () => {
    setResult({
      production: prod,
      jurisdiction: juris,
      budget: 15000000,
      rate: 20,
      estimated: 3000000,
      minSpend: 500000,
      qualified: true,
    });
  };

  return (
    <div style={{ padding: 32 }}>
      <h1 style={{ fontSize: 26, fontWeight: 700, color: COLORS.text, margin: "0 0 24px", letterSpacing: "-0.5px" }}>Incentive Calculator</h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.5fr", gap: 24 }}>
        {/* Form */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${COLORS.cardBorder}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
            <Calculator size={18} color={COLORS.accent} />
            <span style={{ fontWeight: 700, fontSize: 16, color: COLORS.text }}>Quick Estimate</span>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Production</label>
            <select value={prod} onChange={e => setProd(e.target.value)} style={{ width: "100%", border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, color: COLORS.text, background: "#fff" }}>
              {productions.map(p => <option key={p.id}>{p.title}</option>)}
            </select>
          </div>
          <div style={{ marginBottom: 24 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Jurisdiction</label>
            <select value={juris} onChange={e => setJuris(e.target.value)} style={{ width: "100%", border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, color: COLORS.text, background: "#fff" }}>
              {jurisdictions.map(j => <option key={j.state}>{j.state}</option>)}
            </select>
          </div>
          <button onClick={run} style={{ width: "100%", background: COLORS.accent, color: "#fff", border: "none", borderRadius: 8, padding: "12px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
            Run Calculation
          </button>
        </div>

        {/* Result */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${COLORS.cardBorder}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
          {!result ? (
            <div style={{ textAlign: "center", color: COLORS.textLight }}>
              <Calculator size={40} style={{ marginBottom: 12, opacity: 0.3 }} />
              <div style={{ fontSize: 14 }}>Select project details to run estimate.</div>
            </div>
          ) : (
            <div style={{ width: "100%" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: COLORS.success }} />
                <span style={{ fontSize: 13, color: COLORS.success, fontWeight: 600 }}>Qualified</span>
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, color: COLORS.text, marginBottom: 4 }}>
                ${(result.estimated / 1000000).toFixed(1)}M Estimated Credit
              </div>
              <div style={{ fontSize: 13, color: COLORS.textMuted, marginBottom: 24 }}>{result.rate}% base rate · {result.jurisdiction}</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                {[["Production", result.production], ["Budget", `$${(result.budget/1000000).toFixed(0)}M`], ["Rate", `${result.rate}%`], ["Min Spend", `$${(result.minSpend/1000).toFixed(0)}K`]].map(([k, v]) => (
                  <div key={k} style={{ background: COLORS.mainBg, borderRadius: 8, padding: "12px 14px" }}>
                    <div style={{ fontSize: 11, color: COLORS.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>{k}</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: COLORS.text }}>{v}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function JurisdictionsView() {
  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 24 }}>
        {/* Left panel */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {/* Regulatory Feed */}
          <div style={{ background: COLORS.sidebar, borderRadius: 12, overflow: "hidden" }}>
            <div style={{ background: "#1e2535", padding: "12px 16px", display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#ef4444", animation: "pulse 2s infinite" }} />
              <span style={{ color: "#e2e8f0", fontSize: 12, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" }}>Regulatory Feed</span>
            </div>
            <div style={{ padding: "12px 16px" }}>
              {regulatoryFeed.map((item, i) => (
                <div key={i} style={{ marginBottom: i < regulatoryFeed.length - 1 ? 14 : 0, paddingBottom: i < regulatoryFeed.length - 1 ? 14 : 0, borderBottom: i < regulatoryFeed.length - 1 ? "1px solid #1e2535" : "none" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ color: COLORS.accent, fontSize: 12, fontWeight: 600 }}>{item.source}</span>
                    <span style={{ color: "#475569", fontSize: 11 }}>{item.time}</span>
                  </div>
                  <p style={{ color: "#94a3b8", fontSize: 12, margin: 0, lineHeight: 1.5 }}>{item.text}</p>
                </div>
              ))}
              <div style={{ marginTop: 12, fontSize: 11, color: "#475569", textAlign: "center", fontWeight: 600, letterSpacing: "0.05em" }}>GLOBAL MONITORING ACTIVE</div>
            </div>
          </div>

          {/* Agency Directory */}
          <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1px solid ${COLORS.cardBorder}` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
              <Briefcase size={15} color={COLORS.accent} />
              <span style={{ fontWeight: 700, fontSize: 14, color: COLORS.text }}>Agency Directory</span>
            </div>
            <p style={{ fontSize: 13, color: COLORS.textMuted, lineHeight: 1.6, marginBottom: 16 }}>
              PilotForge connects with over 400 jurisdictions globally. Contact our concierge for help with custom applications.
            </p>
            <button style={{ width: "100%", border: `1px solid ${COLORS.cardBorder}`, background: "#fff", borderRadius: 8, padding: "10px", fontSize: 13, fontWeight: 600, color: COLORS.accent, cursor: "pointer" }}>
              Contact Concierge
            </button>
          </div>
        </div>

        {/* Right panel */}
        <div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 4 }}>
              <h1 style={{ fontSize: 28, fontWeight: 800, color: COLORS.text, margin: 0, letterSpacing: "-0.5px", lineHeight: 1.2 }}>Jurisdiction<br />Intelligence</h1>
              <div style={{ display: "flex", gap: 10 }}>
                <select style={{ border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "8px 12px", fontSize: 13, background: "#fff" }}><option>All Types</option></select>
                <select style={{ border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "8px 12px", fontSize: 13, background: "#fff" }}><option>All Countries</option></select>
                <div style={{ border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "8px 12px", display: "flex", alignItems: "center", gap: 6, background: "#fff" }}>
                  <Search size={13} color={COLORS.textMuted} />
                  <input placeholder="Search by name or agen..." style={{ border: "none", outline: "none", fontSize: 13, width: 160, color: COLORS.text }} />
                </div>
              </div>
            </div>
            <p style={{ color: COLORS.textMuted, fontSize: 13, marginTop: 8 }}>Explore and filter international tax incentive profiles.</p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
            {jurisdictions.map((j, i) => (
              <div key={i} style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1px solid ${COLORS.cardBorder}` }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <span style={{ background: COLORS.mainBg, borderRadius: 4, padding: "2px 6px", fontSize: 11, fontWeight: 700, color: COLORS.textMuted }}>{j.code}</span>
                    <span style={{ fontSize: 16, fontWeight: 700, color: COLORS.text }}>{j.state}</span>
                  </div>
                  <span style={{ background: "#dcfce7", color: "#15803d", fontSize: 11, fontWeight: 700, padding: "3px 8px", borderRadius: 6 }}>{j.base}</span>
                </div>
                <div style={{ marginBottom: 8 }}>
                  <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 2 }}>Agency</div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: COLORS.text }}>{j.agency}</div>
                </div>
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 2 }}>Min Spend</div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: COLORS.text }}>{j.minSpend}</div>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <button style={{ background: "none", border: "none", fontSize: 12, fontWeight: 700, color: COLORS.textMuted, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
                    REVIEW <ChevronRight size={12} />
                  </button>
                  <button style={{ background: "none", border: "none", fontSize: 12, fontWeight: 700, color: COLORS.accent, cursor: "pointer" }}>
                    ADD TO PRODUCTION
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function AdvisorView() {
  const [synopsis, setSynopsis] = useState("");
  const [budget, setBudget] = useState("1000000");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!synopsis.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{
            role: "user",
            content: `You are a film tax incentive advisor. Given this project synopsis and budget, recommend the top 3 US states or international jurisdictions and explain why. Be specific about incentive rates and qualifying criteria.\n\nSynopsis: ${synopsis}\nBudget: $${parseInt(budget).toLocaleString()}\n\nRespond in JSON only: {"recommendations": [{"jurisdiction": "string", "rate": "string", "estimated_credit": "string", "reason": "string", "best_for": "string"}]}`
          }]
        })
      });
      const data = await response.json();
      const text = data.content[0].text;
      const clean = text.replace(/```json|```/g, "").trim();
      setResult(JSON.parse(clean));
    } catch (e) {
      setResult({ error: "Could not generate insights. Please try again." });
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 32 }}>
      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <div style={{ width: 56, height: 56, borderRadius: 16, background: "#dbeafe", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
          <Bot size={28} color={COLORS.accent} />
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: COLORS.text, margin: "0 0 8px", letterSpacing: "-0.5px" }}>AI Strategic Advisor</h1>
        <p style={{ color: COLORS.textMuted, fontSize: 14, margin: 0 }}>Get instant jurisdiction recommendations based on your project synopsis.</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: 24, maxWidth: 900, margin: "0 auto" }}>
        {/* Input */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${COLORS.cardBorder}` }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Synopsis</label>
            <textarea value={synopsis} onChange={e => setSynopsis(e.target.value)} placeholder="Enter project summary..." rows={6}
              style={{ width: "100%", border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, color: COLORS.text, resize: "vertical", fontFamily: "inherit", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Total Budget (USD)</label>
            <input value={budget} onChange={e => setBudget(e.target.value)} type="number"
              style={{ width: "100%", border: `1px solid ${COLORS.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, color: COLORS.text, boxSizing: "border-box" }} />
          </div>
          <button onClick={generate} disabled={loading || !synopsis.trim()}
            style={{ width: "100%", background: loading || !synopsis.trim() ? "#94a3b8" : COLORS.accent, color: "#fff", border: "none", borderRadius: 8, padding: "12px", fontSize: 14, fontWeight: 600, cursor: loading || !synopsis.trim() ? "not-allowed" : "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
            {loading ? <><RefreshCw size={16} style={{ animation: "spin 1s linear infinite" }} /> Analyzing...</> : <><Bot size={16} /> Generate Insights</>}
          </button>
        </div>

        {/* Results */}
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${COLORS.cardBorder}`, display: "flex", alignItems: result ? "flex-start" : "center", justifyContent: "center" }}>
          {!result && !loading && (
            <div style={{ textAlign: "center", color: COLORS.textLight }}>
              <Bot size={40} style={{ marginBottom: 12, opacity: 0.3 }} />
              <div style={{ fontSize: 14 }}>Submit project details to reveal strategic recommendations.</div>
            </div>
          )}
          {loading && (
            <div style={{ textAlign: "center", color: COLORS.textMuted, width: "100%" }}>
              <RefreshCw size={32} style={{ marginBottom: 12, opacity: 0.5, animation: "spin 1s linear infinite" }} />
              <div style={{ fontSize: 14 }}>Analyzing incentive landscape...</div>
            </div>
          )}
          {result?.error && <div style={{ color: COLORS.danger, fontSize: 14 }}>{result.error}</div>}
          {result?.recommendations && (
            <div style={{ width: "100%" }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: COLORS.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 16 }}>Top Recommendations</div>
              {result.recommendations.map((r, i) => (
                <div key={i} style={{ background: COLORS.mainBg, borderRadius: 10, padding: 16, marginBottom: 12, borderLeft: `3px solid ${COLORS.accent}` }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontWeight: 700, fontSize: 15, color: COLORS.text }}>{r.jurisdiction}</span>
                    <span style={{ background: "#dcfce7", color: "#15803d", fontSize: 12, fontWeight: 700, padding: "2px 8px", borderRadius: 6 }}>{r.rate}</span>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: COLORS.accent, marginBottom: 6 }}>Est. Credit: {r.estimated_credit}</div>
                  <div style={{ fontSize: 12, color: COLORS.textMuted, lineHeight: 1.5 }}>{r.reason}</div>
                  {r.best_for && <div style={{ fontSize: 11, color: COLORS.textLight, marginTop: 6, fontStyle: "italic" }}>Best for: {r.best_for}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}