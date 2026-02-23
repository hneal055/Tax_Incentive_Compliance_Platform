import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import {
  LayoutDashboard, Film, Calculator, Globe, Bot, Settings,
  RefreshCw, Plus, ChevronRight, AlertCircle, TrendingUp,
  Briefcase, DollarSign, Search, ExternalLink
} from "lucide-react";

const API = import.meta.env.VITE_API_URL || "https://pilotforge-5wiz.onrender.com";

const C = {
  sidebar: "#161b27", sidebarBorder: "#1e2535",
  cardBorder: "#e5e9f0", accent: "#0ea5e9",
  accentGlow: "rgba(14,165,233,0.15)", success: "#10b981",
  danger: "#ef4444", text: "#0f172a",
  textMuted: "#64748b", textLight: "#94a3b8", mainBg: "#f1f5f9",
};

interface Jurisdiction {
  id: string; name: string; code: string; country: string;
  type: string; description: string; website: string; active: boolean;
}
interface IncentiveRule {
  id: string; jurisdictionId: string; ruleName: string; ruleCode: string;
  incentiveType: string; percentage: number; minSpend: number;
  maxCredit: number | null; requirements: string; active: boolean;
}
interface Production {
  id: string; title: string; productionType: string; status: string;
  budget: number; location: string; jurisdictionId?: string;
}
interface CalcResult {
  production: string; jurisdiction: string; budget: number;
  rate: number; estimated: number; minSpend: number; qualified: boolean;
}
interface AIResult {
  recommendations?: { jurisdiction: string; rate: string; estimated_credit: string; reason: string; best_for?: string }[];
  error?: string;
}

async function apiFetch(path: string) {
  const r = await fetch(`${API}${path}`);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export default function PilotForgeDashboard() {
  const [active, setActive] = useState("dashboard");
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [rules, setRules] = useState<IncentiveRule[]>([]);
  const [productions, setProductions] = useState<Production[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [jData, rData, pData] = await Promise.allSettled([
          apiFetch("/api/v1/jurisdictions?limit=100"),
          apiFetch("/api/v1/incentive-rules/?limit=100"),
          apiFetch("/api/v1/productions"),
        ]);
        if (jData.status === "fulfilled") setJurisdictions(jData.value.jurisdictions || []);
        if (rData.status === "fulfilled") setRules(rData.value.rules || rData.value || []);
        if (pData.status === "fulfilled") setProductions(pData.value.productions || pData.value || []);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "productions", label: "Productions", icon: Film },
    { id: "calculator", label: "Incentive Calculator", icon: Calculator },
    { id: "jurisdictions", label: "Jurisdictions", icon: Globe },
    { id: "advisor", label: "AI Advisor", icon: Bot, badge: "NEW" },
  ];

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "'DM Sans','Segoe UI',sans-serif", background: C.mainBg }}>
      <div style={{ width: 220, background: C.sidebar, borderRight: `1px solid ${C.sidebarBorder}`, display: "flex", flexDirection: "column", flexShrink: 0 }}>
        <div style={{ padding: "20px 16px", display: "flex", alignItems: "center", gap: 10, borderBottom: `1px solid ${C.sidebarBorder}` }}>
          <div style={{ width: 36, height: 36, background: C.accent, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <DollarSign size={20} color="#fff" />
          </div>
          <span style={{ color: "#fff", fontWeight: 700, fontSize: 18, letterSpacing: "-0.3px" }}>PilotForge</span>
        </div>
        <nav style={{ flex: 1, padding: "12px 8px" }}>
          {navItems.map(({ id, label, icon: Icon, badge }) => {
            const on = active === id;
            return (
              <button key={id} onClick={() => setActive(id)} style={{
                width: "100%", display: "flex", alignItems: "center", gap: 10,
                padding: "9px 12px", borderRadius: 8, border: "none", cursor: "pointer",
                background: on ? C.accentGlow : "transparent",
                color: on ? C.accent : "#94a3b8", fontSize: 14, fontWeight: on ? 600 : 400,
                marginBottom: 2, textAlign: "left",
                borderLeft: on ? `3px solid ${C.accent}` : "3px solid transparent",
              }}>
                <Icon size={17} /><span style={{ flex: 1 }}>{label}</span>
                {badge && <span style={{ fontSize: 10, background: C.accent, color: "#fff", padding: "2px 6px", borderRadius: 4, fontWeight: 700 }}>{badge}</span>}
              </button>
            );
          })}
        </nav>
        <div style={{ padding: "12px 16px", borderTop: `1px solid ${C.sidebarBorder}`, display: "flex", alignItems: "center", gap: 10 }}>
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

      <div style={{ flex: 1, overflow: "auto" }}>
        {loading ? (
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100%", color: C.textMuted, gap: 12 }}>
            <RefreshCw size={20} style={{ animation: "spin 1s linear infinite" }} /> Loading PilotForge data...
            <style>{`@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}`}</style>
          </div>
        ) : (
          <>
            {active === "dashboard" && <DashboardView productions={productions} rules={rules} jurisdictions={jurisdictions} />}
            {active === "productions" && <ProductionsView productions={productions} jurisdictions={jurisdictions} setProductions={setProductions} />}
            {active === "calculator" && <CalculatorView productions={productions} jurisdictions={jurisdictions} rules={rules} />}
            {active === "jurisdictions" && <JurisdictionsView jurisdictions={jurisdictions} />}
            {active === "advisor" && <AdvisorView />}
          </>
        )}
      </div>
    </div>
  );
}

function MetricCard({ label, value, sub, icon, iconBg }: { label: string; value: string; sub: string; icon: React.ReactNode; iconBg: string }) {
  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: "20px 24px", border: `1px solid ${C.cardBorder}`, display: "flex", alignItems: "center", justifyContent: "space-between", flex: 1 }}>
      <div>
        <div style={{ color: C.textMuted, fontSize: 12, fontWeight: 500, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>{label}</div>
        <div style={{ color: C.text, fontSize: 26, fontWeight: 700, letterSpacing: "-0.5px" }}>{value}</div>
        <div style={{ color: C.textLight, fontSize: 12, marginTop: 4 }}>{sub}</div>
      </div>
      <div style={{ width: 44, height: 44, borderRadius: 10, background: iconBg, display: "flex", alignItems: "center", justifyContent: "center" }}>{icon}</div>
    </div>
  );
}

function DashboardView({ productions, rules, jurisdictions }: { productions: Production[]; rules: IncentiveRule[]; jurisdictions: Jurisdiction[] }) {
  const totalBudget = productions.reduce((s, p) => s + (p.budget || 0), 0);
  const avgRate = rules.length ? rules.reduce((s, r) => s + r.percentage, 0) / rules.length : 0;
  const estCredits = totalBudget * (avgRate / 100);

  const chartData = productions.slice(0, 5).map(p => ({
    name: p.title.length > 14 ? p.title.slice(0, 14) + "..." : p.title,
    budget: p.budget || 0,
    estimated: Math.round((p.budget || 0) * (avgRate / 100)),
  }));

  const fmt = (n: number) => n >= 1000000 ? `$${(n / 1000000).toFixed(1)}M` : n >= 1000 ? `$${(n / 1000).toFixed(0)}K` : `$${n}`;

  return (
    <div style={{ padding: 32 }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 26, fontWeight: 700, color: C.text, margin: 0, letterSpacing: "-0.5px" }}>Executive Dashboard</h1>
        <p style={{ color: C.textMuted, fontSize: 14, marginTop: 4 }}>Overview of active productions and tax incentive performance.</p>
      </div>
      <div style={{ display: "flex", gap: 16, marginBottom: 28 }}>
        <MetricCard label="Budget Volume" value={fmt(totalBudget)} sub="Total planned" iconBg="#dbeafe" icon={<Briefcase size={20} color="#3b82f6" />} />
        <MetricCard label="Est. Tax Credits" value={fmt(estCredits)} sub={`Avg ${avgRate.toFixed(0)}% rate`} iconBg="#dcfce7" icon={<TrendingUp size={20} color="#10b981" />} />
        <MetricCard label="Active Projects" value={String(productions.length)} sub="Tracked productions" iconBg="#f3e8ff" icon={<Film size={20} color="#8b5cf6" />} />
        <MetricCard label="Jurisdictions" value={String(jurisdictions.length)} sub="Programs available" iconBg="#fef3c7" icon={<AlertCircle size={20} color="#f59e0b" />} />
      </div>
      {chartData.length > 0 ? (
        <div style={{ background: "#fff", borderRadius: 12, padding: 24, border: `1px solid ${C.cardBorder}` }}>
          <h2 style={{ fontSize: 16, fontWeight: 700, color: C.text, marginTop: 0, marginBottom: 20 }}>Budget vs. Estimated Credits</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={chartData} barGap={4}>
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: C.textMuted }} axisLine={false} tickLine={false} />
              <YAxis tickFormatter={(v: number) => `$${(v / 1000000).toFixed(0)}M`} tick={{ fontSize: 12, fill: C.textMuted }} axisLine={false} tickLine={false} />
              <Tooltip formatter={(v: number) => fmt(v)} contentStyle={{ borderRadius: 8, border: "1px solid #e2e8f0", fontSize: 13 }} />
              <Legend wrapperStyle={{ fontSize: 13, paddingTop: 16 }} />
              <Bar dataKey="budget" name="Budget" fill="#38bdf8" radius={[4, 4, 0, 0]} />
              <Bar dataKey="estimated" name="Est. Credit" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div style={{ background: "#fff", borderRadius: 12, padding: 40, border: `1px solid ${C.cardBorder}`, textAlign: "center", color: C.textMuted }}>
          <Film size={40} style={{ opacity: 0.2, marginBottom: 12 }} />
          <div style={{ fontSize: 14 }}>No productions yet. Add your first production to see budget analytics.</div>
        </div>
      )}
    </div>
  );
}

function ProductionsView({ productions, jurisdictions, setProductions }: {
  productions: Production[]; jurisdictions: Jurisdiction[];
  setProductions: React.Dispatch<React.SetStateAction<Production[]>>;
}) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", productionType: "feature_film", status: "development", budget: "", location: "", jurisdictionId: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [typeFilter, setTypeFilter] = useState("all");

  const statusColors: Record<string, string> = {
    production: "#0ea5e9", development: "#8b5cf6", released: "#10b981",
    post_production: "#f59e0b", pre_production: "#6366f1",
  };

  const filtered = productions.filter(p => {
    const s = (p.status || "").toLowerCase();
    const t = (p.productionType || "").toLowerCase();
    if (statusFilter !== "all" && s !== statusFilter) return false;
    if (typeFilter !== "all" && t !== typeFilter) return false;
    return true;
  });

  const save = async () => {
    if (!form.title.trim()) { setError("Title is required"); return; }
    setSaving(true); setError("");
    try {
      const res = await fetch(`${API}/api/v1/productions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, budget: parseFloat(form.budget) || 0 }),
      });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Failed"); }
      const created = await res.json();
      setProductions(prev => [...prev, created]);
      setShowForm(false);
      setForm({ title: "", productionType: "feature_film", status: "development", budget: "", location: "", jurisdictionId: "" });
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error saving production");
    } finally { setSaving(false); }
  };

  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24 }}>
        <h1 style={{ fontSize: 26, fontWeight: 700, color: C.text, margin: 0, letterSpacing: "-0.5px" }}>Productions</h1>
        <button onClick={() => setShowForm(!showForm)} style={{ display: "flex", alignItems: "center", gap: 8, background: C.accent, color: "#fff", border: "none", borderRadius: 8, padding: "10px 18px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
          <Plus size={16} /> New Production
        </button>
      </div>

      {showForm && (
        <div style={{ background: "#fff", borderRadius: 12, padding: 24, border: `1px solid ${C.cardBorder}`, marginBottom: 20 }}>
          <h3 style={{ margin: "0 0 16px", fontSize: 15, fontWeight: 700, color: C.text }}>New Production</h3>
          {error && <div style={{ background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, padding: "10px 14px", color: C.danger, fontSize: 13, marginBottom: 14 }}>{error}</div>}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            {[
              { label: "Title *", key: "title", type: "text", placeholder: "e.g. The Silent Horizon" },
              { label: "Budget (USD)", key: "budget", type: "number", placeholder: "e.g. 5000000" },
              { label: "Location", key: "location", type: "text", placeholder: "e.g. Georgia" },
            ].map(f => (
              <div key={f.key}>
                <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>{f.label}</label>
                <input type={f.type} placeholder={f.placeholder} value={(form as Record<string, string>)[f.key]}
                  onChange={e => setForm(prev => ({ ...prev, [f.key]: e.target.value }))}
                  style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "9px 12px", fontSize: 13, boxSizing: "border-box" }} />
              </div>
            ))}
            <div>
              <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Type</label>
              <select value={form.productionType} onChange={e => setForm(p => ({ ...p, productionType: e.target.value }))}
                style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "9px 12px", fontSize: 13 }}>
                <option value="feature_film">Feature Film</option>
                <option value="television_series">Television Series</option>
                <option value="documentary">Documentary</option>
                <option value="commercial">Commercial</option>
                <option value="short_film">Short Film</option>
              </select>
            </div>
            <div>
              <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Status</label>
              <select value={form.status} onChange={e => setForm(p => ({ ...p, status: e.target.value }))}
                style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "9px 12px", fontSize: 13 }}>
                <option value="development">Development</option>
                <option value="pre_production">Pre-Production</option>
                <option value="production">Production</option>
                <option value="post_production">Post-Production</option>
                <option value="released">Released</option>
              </select>
            </div>
            <div>
              <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Jurisdiction</label>
              <select value={form.jurisdictionId} onChange={e => setForm(p => ({ ...p, jurisdictionId: e.target.value }))}
                style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "9px 12px", fontSize: 13 }}>
                <option value="">None selected</option>
                {jurisdictions.map(j => <option key={j.id} value={j.id}>{j.name}</option>)}
              </select>
            </div>
          </div>
          <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
            <button onClick={save} disabled={saving} style={{ background: C.accent, color: "#fff", border: "none", borderRadius: 8, padding: "10px 20px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
              {saving ? "Saving..." : "Create Production"}
            </button>
            <button onClick={() => { setShowForm(false); setError(""); }} style={{ background: "none", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "10px 20px", fontSize: 13, cursor: "pointer", color: C.textMuted }}>
              Cancel
            </button>
          </div>
        </div>
      )}

      <div style={{ background: "#fff", borderRadius: 12, padding: "14px 20px", border: `1px solid ${C.cardBorder}`, marginBottom: 20, display: "flex", alignItems: "center", gap: 16 }}>
        <div>
          <div style={{ fontSize: 10, color: C.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Status</div>
          <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} style={{ border: `1px solid ${C.cardBorder}`, borderRadius: 6, padding: "6px 10px", fontSize: 13 }}>
            <option value="all">All Statuses</option>
            <option value="development">Development</option>
            <option value="pre_production">Pre-Production</option>
            <option value="production">Production</option>
            <option value="post_production">Post-Production</option>
            <option value="released">Released</option>
          </select>
        </div>
        <div>
          <div style={{ fontSize: 10, color: C.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Type</div>
          <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} style={{ border: `1px solid ${C.cardBorder}`, borderRadius: 6, padding: "6px 10px", fontSize: 13 }}>
            <option value="all">All Types</option>
            <option value="feature_film">Feature Film</option>
            <option value="television_series">Television Series</option>
            <option value="documentary">Documentary</option>
            <option value="commercial">Commercial</option>
          </select>
        </div>
        <div style={{ marginLeft: "auto", color: C.textMuted, fontSize: 13 }}>{filtered.length} Project{filtered.length !== 1 ? "s" : ""} Tracked</div>
      </div>

      {filtered.length === 0 ? (
        <div style={{ background: "#fff", borderRadius: 12, padding: 40, border: `1px solid ${C.cardBorder}`, textAlign: "center", color: C.textMuted }}>
          <Film size={40} style={{ opacity: 0.2, marginBottom: 12 }} />
          <div style={{ fontSize: 14 }}>No productions found. Click "New Production" to add one.</div>
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: 16 }}>
          {filtered.map(p => {
            const s = (p.status || "development").toLowerCase();
            const color = statusColors[s] || C.textMuted;
            const budget = p.budget >= 1000000 ? `$${(p.budget / 1000000).toFixed(1)}M` : p.budget >= 1000 ? `$${(p.budget / 1000).toFixed(0)}K` : `$${p.budget || 0}`;
            return (
              <div key={p.id} style={{ background: "#fff", borderRadius: 12, padding: 24, border: `1px solid ${C.cardBorder}`, cursor: "pointer" }}
                onMouseEnter={e => (e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,0.08)")}
                onMouseLeave={e => (e.currentTarget.style.boxShadow = "none")}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                  <Film size={18} color={C.textLight} />
                  <span style={{ fontSize: 11, fontWeight: 700, color, letterSpacing: "0.05em", textTransform: "uppercase" }}>{p.status}</span>
                </div>
                <div style={{ fontSize: 17, fontWeight: 700, color: C.text, marginBottom: 4 }}>{p.title}</div>
                <div style={{ fontSize: 13, color: C.textMuted, marginBottom: 16 }}>{(p.productionType || "").replace(/_/g, " ")}</div>
                <div style={{ display: "flex", gap: 16 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 4, color: C.textMuted, fontSize: 13 }}><DollarSign size={13} />{budget}</div>
                  {p.location && <div style={{ display: "flex", alignItems: "center", gap: 4, color: C.textMuted, fontSize: 13 }}><Globe size={13} />{p.location}</div>}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function CalculatorView({ productions, jurisdictions, rules }: { productions: Production[]; jurisdictions: Jurisdiction[]; rules: IncentiveRule[] }) {
  const [prodId, setProdId] = useState(productions[0]?.id || "");
  const [jurisId, setJurisId] = useState(jurisdictions[0]?.id || "");
  const [result, setResult] = useState<CalcResult | null>(null);

  const run = () => {
    const prod = productions.find(p => p.id === prodId);
    const juris = jurisdictions.find(j => j.id === jurisId);
    const rule = rules.find(r => r.jurisdictionId === jurisId && r.active);
    if (!prod || !juris) return;
    const rate = rule?.percentage || 20;
    const minSpend = rule?.minSpend || 0;
    const qualified = prod.budget >= minSpend;
    setResult({
      production: prod.title, jurisdiction: juris.name,
      budget: prod.budget, rate, minSpend,
      estimated: qualified ? Math.round(prod.budget * (rate / 100)) : 0, qualified,
    });
  };

  const fmt = (n: number) => n >= 1000000 ? `$${(n / 1000000).toFixed(1)}M` : `$${(n / 1000).toFixed(0)}K`;

  return (
    <div style={{ padding: 32 }}>
      <h1 style={{ fontSize: 26, fontWeight: 700, color: C.text, margin: "0 0 24px", letterSpacing: "-0.5px" }}>Incentive Calculator</h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.5fr", gap: 24 }}>
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${C.cardBorder}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
            <Calculator size={18} color={C.accent} />
            <span style={{ fontWeight: 700, fontSize: 16, color: C.text }}>Quick Estimate</span>
          </div>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Production</label>
            {productions.length === 0 ? (
              <div style={{ fontSize: 13, color: C.textMuted, padding: "10px 12px", background: C.mainBg, borderRadius: 8 }}>No productions yet — add one first.</div>
            ) : (
              <select value={prodId} onChange={e => setProdId(e.target.value)} style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13 }}>
                {productions.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
              </select>
            )}
          </div>
          <div style={{ marginBottom: 24 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Jurisdiction</label>
            <select value={jurisId} onChange={e => setJurisId(e.target.value)} style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13 }}>
              {jurisdictions.map(j => <option key={j.id} value={j.id}>{j.name} ({j.code})</option>)}
            </select>
          </div>
          <button onClick={run} disabled={!prodId || !jurisId} style={{ width: "100%", background: C.accent, color: "#fff", border: "none", borderRadius: 8, padding: "12px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
            Run Calculation
          </button>
        </div>
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${C.cardBorder}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
          {!result ? (
            <div style={{ textAlign: "center", color: C.textLight }}>
              <Calculator size={40} style={{ marginBottom: 12, opacity: 0.3 }} />
              <div style={{ fontSize: 14 }}>Select project details to run estimate.</div>
            </div>
          ) : (
            <div style={{ width: "100%" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: result.qualified ? C.success : C.danger }} />
                <span style={{ fontSize: 13, color: result.qualified ? C.success : C.danger, fontWeight: 600 }}>
                  {result.qualified ? "Qualified" : `Below minimum spend (${fmt(result.minSpend)} required)`}
                </span>
              </div>
              <div style={{ fontSize: 22, fontWeight: 700, color: C.text, marginBottom: 4 }}>{fmt(result.estimated)} Estimated Credit</div>
              <div style={{ fontSize: 13, color: C.textMuted, marginBottom: 24 }}>{result.rate}% base rate · {result.jurisdiction}</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                {[["Production", result.production], ["Budget", fmt(result.budget)], ["Rate", `${result.rate}%`], ["Min Spend", fmt(result.minSpend)]].map(([k, v]) => (
                  <div key={k} style={{ background: C.mainBg, borderRadius: 8, padding: "12px 14px" }}>
                    <div style={{ fontSize: 11, color: C.textMuted, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>{k}</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: C.text }}>{v}</div>
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

function JurisdictionsView({ jurisdictions }: { jurisdictions: Jurisdiction[] }) {
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");

  const filtered = jurisdictions.filter(j => {
    const q = search.toLowerCase();
    const match = j.name.toLowerCase().includes(q) || j.code.toLowerCase().includes(q);
    const type = typeFilter === "all" || j.type === typeFilter;
    return match && type;
  });

  const regulatoryFeed = [
    { source: "California Film Commission", time: "2h ago", text: "Proposed expansion of the 30-mile studio zone currently under committee review." },
    { source: "British Film Commission", time: "5h ago", text: "New guidance issued for VFX expenditure qualification under updates." },
    { source: "Georgia Dept. of Econ Dev", time: "1d ago", text: "Fiscal year cap status: 65% utilized. Applications open." },
  ];

  return (
    <div style={{ padding: 32 }}>
      <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 24 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ background: "#161b27", borderRadius: 12, overflow: "hidden" }}>
            <div style={{ background: "#1e2535", padding: "12px 16px", display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: C.danger }} />
              <span style={{ color: "#e2e8f0", fontSize: 12, fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" }}>Regulatory Feed</span>
            </div>
            <div style={{ padding: "12px 16px" }}>
              {regulatoryFeed.map((item, i) => (
                <div key={i} style={{ marginBottom: i < 2 ? 14 : 0, paddingBottom: i < 2 ? 14 : 0, borderBottom: i < 2 ? "1px solid #1e2535" : "none" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ color: C.accent, fontSize: 12, fontWeight: 600 }}>{item.source}</span>
                    <span style={{ color: "#475569", fontSize: 11 }}>{item.time}</span>
                  </div>
                  <p style={{ color: "#94a3b8", fontSize: 12, margin: 0, lineHeight: 1.5 }}>{item.text}</p>
                </div>
              ))}
              <div style={{ marginTop: 12, fontSize: 11, color: "#475569", textAlign: "center", fontWeight: 600 }}>GLOBAL MONITORING ACTIVE</div>
            </div>
          </div>
          <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1px solid ${C.cardBorder}` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
              <Briefcase size={15} color={C.accent} />
              <span style={{ fontWeight: 700, fontSize: 14, color: C.text }}>Agency Directory</span>
            </div>
            <p style={{ fontSize: 13, color: C.textMuted, lineHeight: 1.6, marginBottom: 16 }}>
              PilotForge tracks {jurisdictions.length} active U.S. incentive programs. International jurisdictions coming soon.
            </p>
          </div>
        </div>

        <div>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 16 }}>
            <div>
              <h1 style={{ fontSize: 28, fontWeight: 800, color: C.text, margin: 0, letterSpacing: "-0.5px", lineHeight: 1.2 }}>Jurisdiction<br />Intelligence</h1>
              <p style={{ color: C.textMuted, fontSize: 13, marginTop: 8 }}>Explore and filter tax incentive profiles. {filtered.length} programs shown.</p>
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} style={{ border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "8px 12px", fontSize: 13, background: "#fff" }}>
                <option value="all">All Types</option>
                <option value="state">States</option>
                <option value="district">Districts</option>
              </select>
              <div style={{ border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "8px 12px", display: "flex", alignItems: "center", gap: 6, background: "#fff" }}>
                <Search size={13} color={C.textMuted} />
                <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search jurisdictions..." style={{ border: "none", outline: "none", fontSize: 13, width: 160 }} />
              </div>
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: 14 }}>
            {filtered.map(j => {
              const pct = j.description.match(/(\d+)%/)?.[1];
              return (
                <div key={j.id} style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1px solid ${C.cardBorder}` }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                      <span style={{ background: C.mainBg, borderRadius: 4, padding: "2px 6px", fontSize: 11, fontWeight: 700, color: C.textMuted }}>US</span>
                      <span style={{ fontSize: 15, fontWeight: 700, color: C.text }}>{j.name}</span>
                    </div>
                    {pct && <span style={{ background: "#dcfce7", color: "#15803d", fontSize: 11, fontWeight: 700, padding: "3px 8px", borderRadius: 6 }}>{pct}% BASE</span>}
                  </div>
                  <p style={{ fontSize: 12, color: C.textMuted, margin: "0 0 14px", lineHeight: 1.5 }}>{j.description}</p>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ fontSize: 12, fontWeight: 600, color: C.textLight }}>{j.code} · {j.type}</span>
                    <a href={j.website} target="_blank" rel="noreferrer"
                      style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 12, fontWeight: 700, color: C.accent, textDecoration: "none" }}>
                      Info <ExternalLink size={11} />
                    </a>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function AdvisorView() {
  const [synopsis, setSynopsis] = useState("");
  const [budget, setBudget] = useState("1000000");
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!synopsis.trim()) return;
    setLoading(true); setResult(null);
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{
            role: "user",
            content: `You are a film tax incentive advisor. Given this project synopsis and budget, recommend the top 3 US states or international jurisdictions and explain why. Be specific about incentive rates and qualifying criteria.\n\nSynopsis: ${synopsis}\nBudget: $${parseInt(budget).toLocaleString()}\n\nRespond in JSON only (no markdown): {"recommendations": [{"jurisdiction": "string", "rate": "string", "estimated_credit": "string", "reason": "string", "best_for": "string"}]}`
          }]
        })
      });
      const data = await response.json();
      const text = data.content[0].text;
      const clean = text.replace(/```json|```/g, "").trim();
      setResult(JSON.parse(clean));
    } catch {
      setResult({ error: "Could not generate insights. Please try again." });
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 32 }}>
      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <div style={{ width: 56, height: 56, borderRadius: 16, background: "#dbeafe", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
          <Bot size={28} color={C.accent} />
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 800, color: C.text, margin: "0 0 8px", letterSpacing: "-0.5px" }}>AI Strategic Advisor</h1>
        <p style={{ color: C.textMuted, fontSize: 14, margin: 0 }}>Get instant jurisdiction recommendations based on your project synopsis.</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: 24, maxWidth: 900, margin: "0 auto" }}>
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${C.cardBorder}` }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Synopsis</label>
            <textarea value={synopsis} onChange={e => setSynopsis(e.target.value)} placeholder="Enter project summary..." rows={6}
              style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, resize: "vertical", fontFamily: "inherit", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Total Budget (USD)</label>
            <input value={budget} onChange={e => setBudget(e.target.value)} type="number"
              style={{ width: "100%", border: `1px solid ${C.cardBorder}`, borderRadius: 8, padding: "10px 12px", fontSize: 13, boxSizing: "border-box" }} />
          </div>
          <button onClick={generate} disabled={loading || !synopsis.trim()}
            style={{ width: "100%", background: loading || !synopsis.trim() ? "#94a3b8" : C.accent, color: "#fff", border: "none", borderRadius: 8, padding: "12px", fontSize: 14, fontWeight: 600, cursor: loading || !synopsis.trim() ? "not-allowed" : "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
            {loading ? <><RefreshCw size={16} style={{ animation: "spin 1s linear infinite" }} /> Analyzing...</> : <><Bot size={16} /> Generate Insights</>}
          </button>
        </div>
        <div style={{ background: "#fff", borderRadius: 12, padding: 28, border: `1px solid ${C.cardBorder}`, display: "flex", alignItems: result ? "flex-start" : "center", justifyContent: "center" }}>
          {!result && !loading && (
            <div style={{ textAlign: "center", color: C.textLight }}>
              <Bot size={40} style={{ marginBottom: 12, opacity: 0.3 }} />
              <div style={{ fontSize: 14 }}>Submit project details to reveal strategic recommendations.</div>
            </div>
          )}
          {loading && (
            <div style={{ textAlign: "center", color: C.textMuted, width: "100%" }}>
              <RefreshCw size={32} style={{ marginBottom: 12, opacity: 0.5, animation: "spin 1s linear infinite" }} />
              <div style={{ fontSize: 14 }}>Analyzing incentive landscape...</div>
            </div>
          )}
          {result?.error && <div style={{ color: C.danger, fontSize: 14 }}>{result.error}</div>}
          {result?.recommendations && (
            <div style={{ width: "100%" }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: C.textMuted, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 16 }}>Top Recommendations</div>
              {result.recommendations.map((r, i) => (
                <div key={i} style={{ background: C.mainBg, borderRadius: 10, padding: 16, marginBottom: 12, borderLeft: `3px solid ${C.accent}` }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontWeight: 700, fontSize: 15, color: C.text }}>{r.jurisdiction}</span>
                    <span style={{ background: "#dcfce7", color: "#15803d", fontSize: 12, fontWeight: 700, padding: "2px 8px", borderRadius: 6 }}>{r.rate}</span>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: C.accent, marginBottom: 6 }}>Est. Credit: {r.estimated_credit}</div>
                  <div style={{ fontSize: 12, color: C.textMuted, lineHeight: 1.5 }}>{r.reason}</div>
                  {r.best_for && <div style={{ fontSize: 11, color: C.textLight, marginTop: 6, fontStyle: "italic" }}>Best for: {r.best_for}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <style>{`@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}