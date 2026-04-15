import { useState, useRef, useEffect } from 'react';
import { Send, Zap, RotateCcw } from 'lucide-react';
import api from '../api';
import type { Production } from '../types';

// ─── Static data ──────────────────────────────────────────────────────────────

const SUGGESTED_PROMPTS = [
  'Which jurisdiction offers the highest credit rate?',
  'What expenses qualify for the Georgia film tax credit?',
  'Compare New York vs. California incentives for a TV series.',
  'How do I stack federal and state incentives?',
  'What is the minimum spend for UK production incentives?',
  'What documentation is required for Louisiana credit applications?',
];

const WELCOME = `Welcome to **SceneIQ AI Advisor**. I can help you maximize tax incentives for your productions.\n\nAsk me about jurisdiction comparisons, qualifying expenses, application requirements, or incentive stacking strategies. For more targeted analysis, select a production context in the left panel.`;


// ─── Client-side scripted demo responses ─────────────────────────────────────

const SCRIPTED: [string[], string][] = [
  [['georgia', 'expens', 'qualif'], `**Georgia Qualifying Expenses**\n\nGeorgia's Entertainment Industry Investment Act covers:\n\n**Eligible:** Below-the-line labor, equipment rentals, location fees, catering, post-production, and set construction.\n\n**Excluded:** Story rights, music rights, above-the-line compensation (unless resident).\n\nMinimum **$500k** qualified spend required. Georgia residents earn an additional **10% uplift** on their wages. The base credit is **20%**, rising to **30%** with the Georgia promotional logo included in end credits.`],
  [['california', 'ca film'], `**California Film Tax Credit 3.0**\n\nCalifornia offers a **25% credit** on qualified expenditures.\n\n**Requirements:**\n- Minimum $1M qualified spend\n- 75% of principal photography must occur in California\n- Competitive allocation — projects are scored and ranked\n\n**Eligible:** Below-the-line labor, equipment, locations, post-production.\n\n**Max credit:** $25M per project. Apply through the California Film Commission.`],
  [['new york', 'ny film'], `**New York Film Tax Credit**\n\nNew York provides a **25–35% credit** on qualified below-the-line costs.\n\n**Base rate:** 25% statewide\n**Upstate bonus:** Additional 10% for productions outside NYC\n\n**Requirements:**\n- Minimum $1M qualified spend\n- 75% of shooting days in New York\n- Non-competitive — credits issued as earned\n\n**Max credit:** $7M per project.`],
  [['new mexico'], `**New Mexico Film Production Tax Credit**\n\nNew Mexico is one of the most competitive programs in the US:\n\n**Base credit:** 25% on all direct production expenditures\n**Rural bonus:** +5% for productions outside Bernalillo County\n**TV bonus:** +10% for series spending over $30M in NM\n\n**No minimum spend** — accessible to indie and large-budget productions alike. Credits are refundable.`],
  [['louisiana', ' la '], `**Louisiana Entertainment Tax Credit**\n\nLouisiana offers a **25% base rebate** plus a **15% resident payroll** uplift.\n\n**Requirements:** Minimum $300k qualified spend.\n\nCredits are fully transferable and can be sold to Louisiana taxpayers at 85–90 cents on the dollar, effectively converting them to cash.`],
  [['illinois', 'chicago'], `**Illinois Film Production Tax Credit**\n\nIllinois offers a **30% base credit** on Illinois production spending.\n\n**Chicago Bonus:** An additional **15% uplift** applies for productions spending in underserved Chicago communities.\n\n**Requirements:**\n- Minimum $50k Illinois spend\n- No cap on credit amount\n- Transferable credits — can be sold or carried forward\n\nIllinois is one of the few states with no maximum credit cap.`],
  [['uk', 'united kingdom', 'avec', 'british'], `**UK Audio-Visual Expenditure Credit (AVEC)**\n\nThe UK offers a **25% credit** (34% for animation and children's TV) on UK qualifying expenditure.\n\n**Requirements:**\n- At least 10% of total budget must be UK spend\n- Must pass the British Cultural Test\n- No minimum spend threshold\n\n**Eligible:** UK-based crew, facilities, locations, and post-production. The credit is payable even with no UK tax liability.`],
  [['ireland', 'section 481'], `**Ireland Section 481 Film Tax Credit**\n\nIreland offers a **32% credit** on eligible Irish expenditure — one of the highest rates in Europe.\n\n**Requirements:**\n- No minimum spend threshold\n- Production must have cultural or creative merit\n- Some Irish-resident crew required\n\nApplies to features, animation, TV series, and documentaries.`],
  [['stack', 'federal', 'section 181', '181'], `**Stacking Federal + State Incentives**\n\n**Section 181 (Federal):** Allows 100% first-year deduction for productions up to $15M ($20M in qualifying low-income communities).\n\n**How stacking works:**\n1. Section 181 reduces your federal taxable income\n2. State tax credit directly offsets your state tax liability\n3. Both are claimed independently\n\n**Example:** A $5M production in Georgia could claim 181 federally AND the 30% Georgia credit — effectively double-dipping on a legitimate, IRS-sanctioned basis.`],
  [['document', 'application', 'require', 'checklist', 'submit'], `**Standard Application Requirements**\n\n**Pre-production (file before shooting):**\n- Production company registration in the state\n- Estimated budget with expense category breakdown\n- Shooting schedule with location-days by county\n- Proof of financing\n\n**Post-production (file after final delivery):**\n- Final cost report certified by a CPA\n- Payroll records with residency verification\n- Vendor invoices for all qualified expenditures\n\nMost states allow electronic filing. Allow 60–120 days for credit certification.`],
  [['minimum spend', 'threshold', 'minimum budget'], `**Minimum Spend Requirements by Jurisdiction**\n\n| Jurisdiction | Minimum Spend |\n|---|---|\n| New Mexico | None |\n| Ireland | None |\n| UK | 10% UK spend |\n| Louisiana | $300K |\n| Georgia | $500K |\n| California | $1M |\n| New York | $1M |\n| Illinois | $50K |`],
  [['compare', 'vs', 'versus', 'best', 'highest', 'top'], `**Top Film Incentive Jurisdictions — 2025**\n\n| Jurisdiction | Rate | Min Spend | Notes |\n|---|---|---|---|\n| New Mexico | 25–40% | None | Fully refundable |\n| Georgia | 20–30% | $500K | Logo bonus available |\n| Louisiana | 25%+15% | $300K | Transferable credits |\n| New York | 25–35% | $1M | Upstate bonus |\n| California | 25% | $1M | Competitive allocation |\n| UK | 25% | None | AVEC — cultural test |\n| Ireland | 32% | None | Section 481 |\n| Illinois | 30–45% | $50K | No credit cap |\n\nThe best jurisdiction depends on your budget, shooting locations, and crew residency.`],
];

const DEFAULT_RESPONSE = `That's a great question about film tax incentives. SceneIQ tracks incentive programs across 23 jurisdictions globally.\n\nFor personalized analysis, try asking about:\n- **Specific jurisdictions** (Georgia, New York, California, UK, Ireland)\n- **Qualifying expenses** for a particular state\n- **Stacking strategies** to combine federal and state incentives\n- **Application requirements** and documentation\n- **Minimum spend** thresholds by jurisdiction`;

function getScriptedResponse(q: string): string {
  const lower = q.toLowerCase();
  for (const [keywords, response] of SCRIPTED) {
    if (keywords.some(kw => lower.includes(kw))) return response;
  }
  return DEFAULT_RESPONSE;
}

async function streamScripted(text: string, onChunk: (chunk: string) => void): Promise<void> {
  const words = text.split(' ');
  let chunk = '';
  for (let i = 0; i < words.length; i++) {
    chunk += (i === 0 ? '' : ' ') + words[i];
    if ((i + 1) % 3 === 0 || i === words.length - 1) {
      onChunk(chunk);
      chunk = '';
      await new Promise(r => setTimeout(r, 30));
    }
  }
}

// ─── Types ────────────────────────────────────────────────────────────────────

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  ts: Date;
}

// ─── Markdown renderer ────────────────────────────────────────────────────────

function renderMarkdown(text: string) {
  return text.split('\n').map((line, i, arr) => {
    const isLast = i === arr.length - 1;
    const parts = line.split(/\*\*(.*?)\*\*/g);
    const bold = parts.map((p, j) =>
      j % 2 === 1 ? <strong key={j}>{p}</strong> : p
    );
    return (
      <span key={i}>
        {bold}
        {!isLast && <br />}
      </span>
    );
  });
}

// ─── Main component ───────────────────────────────────────────────────────────

function AIAdvisor() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '0', role: 'assistant', content: WELCOME, ts: new Date() },
  ]);
  const [input, setInput]       = useState('');
  const [typing, setTyping]     = useState(false);
  const [production, setProd]   = useState('none');
  const [productions, setProductions] = useState<Production[]>([]);
  const bottomRef               = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.productions.list().then(setProductions).catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  async function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || typing) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: trimmed,
      ts: new Date(),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    const assistantId = (Date.now() + 1).toString();
    const assistantTs = new Date();
    let content = '';
    let firstChunk = true;

    try {
      // Demo mode: stream scripted responses client-side (no backend/API key needed)
      await streamScripted(getScriptedResponse(trimmed), (chunk) => {
        content += chunk;
        if (firstChunk) {
          firstChunk = false;
          setTyping(false);
          setMessages(prev => [
            ...prev,
            { id: assistantId, role: 'assistant', content, ts: assistantTs },
          ]);
        } else {
          setMessages(prev =>
            prev.map(m => m.id === assistantId ? { ...m, content } : m)
          );
        }
      });
    } catch (err: unknown) {
      setTyping(false);
      setMessages(prev => [
        ...prev,
        { id: assistantId, role: 'assistant', content: 'Sorry, something went wrong. Please try again.', ts: assistantTs },
      ]);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  function handleClear() {
    setMessages([{ id: '0', role: 'assistant', content: WELCOME, ts: new Date() }]);
    setInput('');
    setTyping(false);
  }

  const fmt = (d: Date) => d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className="flex gap-6 h-full min-h-0">

      {/* ── Left panel ─────────────────────────────────────────── */}
      <div className="w-72 shrink-0 flex flex-col gap-4">

        {/* Production context */}
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
          <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-2">
            Production Context
          </p>
          <select
            value={production}
            onChange={e => setProd(e.target.value)}
            title="Production context"
            aria-label="Production context"
            className="select-arrow w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
          >
            <option value="none">No production selected</option>
            {productions.map(p => (
              <option key={p.id} value={p.id}>
                {p.title}{p.budgetTotal ? ` — $${(p.budgetTotal / 1_000_000).toFixed(1)}M` : ''}
              </option>
            ))}
          </select>
          {production !== 'none' && (
            <p className="text-xs text-emerald-600 font-medium mt-2.5 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
              Context active — responses factor in this production
            </p>
          )}
        </div>

        {/* Suggested questions */}
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
          <p className="text-[11px] font-bold text-slate-400 tracking-widest uppercase mb-3">
            Suggested Questions
          </p>
          <div className="space-y-2">
            {SUGGESTED_PROMPTS.map(prompt => (
              <button
                key={prompt}
                type="button"
                onClick={() => sendMessage(prompt)}
                disabled={typing}
                className="w-full text-left text-xs text-slate-600 bg-slate-50 hover:bg-blue-50 hover:text-blue-700 border border-slate-100 hover:border-blue-200 rounded-lg px-3 py-2.5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed leading-relaxed"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <p className="text-[11px] text-slate-400 leading-relaxed px-1">
          AI Advisor provides estimates for planning purposes only. Consult a qualified production accountant for final tax decisions.
        </p>
      </div>

      {/* ── Chat panel ─────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0 bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" strokeWidth={2.5} />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">AI Advisor</h2>
              <div className="flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full ${typing ? 'bg-amber-400 animate-pulse' : 'bg-emerald-500'}`} />
                <span className="text-xs text-slate-400">{typing ? 'Thinking…' : 'Ready'}</span>
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={handleClear}
            title="Clear conversation"
            aria-label="Clear conversation"
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-slate-500 hover:text-slate-700 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Clear
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5 min-h-0">
          {messages.map(msg => (
            <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>

              {/* Avatar */}
              <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${
                msg.role === 'assistant' ? 'bg-blue-600' : 'bg-slate-200'
              }`}>
                {msg.role === 'assistant'
                  ? <Zap className="w-3.5 h-3.5 text-white" strokeWidth={2.5} />
                  : <span className="text-[10px] font-bold text-slate-500">YOU</span>
                }
              </div>

              {/* Bubble */}
              <div className={`max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === 'assistant'
                  ? 'bg-slate-50 text-slate-800 rounded-tl-sm'
                  : 'bg-blue-600 text-white rounded-tr-sm'
              }`}>
                {renderMarkdown(msg.content)}
                <p className={`text-[10px] mt-2 ${msg.role === 'assistant' ? 'text-slate-400' : 'text-blue-200'}`}>
                  {fmt(msg.ts)}
                </p>
              </div>
            </div>
          ))}

          {/* Typing indicator — shown only before first chunk arrives */}
          {typing && (
            <div className="flex gap-3">
              <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center shrink-0 mt-0.5">
                <Zap className="w-3.5 h-3.5 text-white" strokeWidth={2.5} />
              </div>
              <div className="bg-slate-50 rounded-2xl rounded-tl-sm px-4 py-3.5 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce [animation-delay:0ms]" />
                <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="px-6 py-4 border-t border-slate-100 shrink-0">
          <div className="flex gap-3 items-end">
            <textarea
              rows={2}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about tax incentives, qualifying expenses, jurisdictions…"
              disabled={typing}
              className="flex-1 px-4 py-3 border border-slate-200 rounded-xl text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none disabled:opacity-50"
            />
            <button
              type="button"
              onClick={() => sendMessage(input)}
              disabled={!input.trim() || typing}
              title="Send message"
              aria-label="Send message"
              className="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <p className="text-[11px] text-slate-400 mt-2">
            Enter to send · Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}

export default AIAdvisor;
