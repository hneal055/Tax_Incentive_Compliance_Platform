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

const WELCOME = `Welcome to **PilotForge AI Advisor**. I can help you maximize tax incentives for your productions.\n\nAsk me about jurisdiction comparisons, qualifying expenses, application requirements, or incentive stacking strategies. For more targeted analysis, select a production context in the left panel.`;

// ─── Types ────────────────────────────────────────────────────────────────────

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  ts: Date;
}

// ─── AI response simulation ───────────────────────────────────────────────────

function getAIResponse(message: string): string {
  const q = message.toLowerCase();

  if (q.includes('highest') || q.includes('best rate') || q.includes('which jurisdiction')) {
    return `Based on current incentive programs, **Ontario, Canada** offers the highest base rate at **35%** on 75% qualified spend — an effective rate of ~26% of total budget.\n\nFor US-only productions:\n\n- **New York** — 30% on ~80% qualified → ~24% effective rate\n- **California** — 25% on ~80% qualified → ~20% effective rate\n- **Louisiana** — 25% on ~85% qualified → ~21% effective rate\n- **Georgia** — 20% on ~85% qualified → ~17% effective rate\n\nNew York and Ontario are the strongest programs right now. New York's credits are **refundable**, meaning you receive cash even with limited state tax liability — a major advantage for independent productions.`;
  }

  if (q.includes('georgia')) {
    return `**Georgia Film Tax Credit — Qualifying Expenses**\n\nQualifying costs under O.C.G.A. § 48-7-40.26:\n\n✓ Cast and crew wages (Georgia residents and non-residents)\n✓ Payments to Georgia-registered vendors\n✓ Equipment rentals sourced within Georgia\n✓ Set construction and strike costs\n✓ Post-production services performed in Georgia\n✓ Lodging for cast and crew on active production days\n\n**Non-qualifying:**\n✗ Story rights and script acquisition\n✗ Marketing and distribution costs\n✗ Bond and insurance premiums\n✗ Financing fees\n\n**Rates:** 20% base, increases to **30%** with the Georgia promotional logo inclusion. Minimum qualified spend: **$500,000** in a single tax year.`;
  }

  if ((q.includes('new york') && q.includes('california')) || q.includes('compare')) {
    return `**New York vs. California — Side by Side**\n\n| | New York | California |\n|---|---|---|\n| Credit Rate | 30% | 25% |\n| Refundable | Yes | No |\n| Transferable | Yes | No |\n| Min Spend | None | $1M |\n| Annual Cap | $420M | $330M |\n| Allocation | First-come | Lottery |\n\n**Bottom line:** New York is more favorable — higher rate, refundable and transferable credits, no minimum spend, and first-come-first-served allocation. California's non-refundable, non-transferable structure limits its value unless your entity has significant California tax liability.\n\nFor TV series, New York adds a **10% pilot bonus** on the first episode.`;
  }

  if (q.includes('stack') || q.includes('federal') || q.includes('combine')) {
    return `**Stacking Federal and State Incentives**\n\nFederal and state incentives can generally be combined — they operate on different mechanisms and do not conflict.\n\n**Federal — Section 181:**\n- 100% first-year deduction on qualified production costs\n- Applies to productions under $15M budget ($20M in low-income areas)\n- This is a **deduction** against income, not a credit\n\n**How stacking works:**\n1. Spend $5M on Georgia-qualified costs\n2. Georgia issues a $1M (20%) tax credit\n3. On the federal return, deduct the full $5M via Section 181\n4. Both benefits apply to the same underlying spend\n\n**Caution:** Some states require reducing qualified costs by federal credits received. Confirm jurisdiction-specific rules with a production accountant before filing.`;
  }

  if (q.includes('uk') || q.includes('united kingdom') || q.includes('british')) {
    return `**UK Audio-Visual Expenditure Credit (AVEC)**\n\nThe UK replaced Film Tax Relief with AVEC in April 2024. Key terms:\n\n- **Rate:** 25% on UK Qualifying Expenditure (UKQE)\n- **Minimum UK spend:** 10% of total production budget\n- **Cap:** None — full credit on all eligible UKQE\n- Administered by HMRC\n\n**Qualifying criteria:**\n✓ Must pass the BFI Cultural Test (or be an official co-production)\n✓ UK-based production company must be the qualifying co-producer\n✓ Intended for theatrical release or BFI-certified streaming\n\n**Why AVEC is more valuable than the old FTR:** It's an above-the-line credit, directly reducing your tax bill rather than enhancing losses. More beneficial for studios and streamers with existing UK tax exposure.`;
  }

  if (q.includes('louisiana') || q.includes('documentation') || q.includes('application') || q.includes('required')) {
    return `**Louisiana Entertainment Incentive — Documentation Checklist**\n\n**Stage 1 — Initial Certification (pre-production):**\n✓ LA Form R-20200 — Entertainment Industry Incentive Application\n✓ Production summary with itemized budget breakdown\n✓ Corporate entity documentation\n✓ Estimated start and wrap dates\n\n**Stage 2 — Final Certification (post-wrap):**\n✓ Certified Audit Report from a Louisiana-licensed CPA\n✓ Final cost report itemized by expense category\n✓ Signed payroll registers for Louisiana residents\n✓ All vendor invoices and receipts\n✓ Proof of production insurance\n\n**Key figures:**\n- Base rate: **25%** + 5% bonus for Louisiana above-the-line residents\n- Minimum spend: **$300,000**\n- Project cap: $150M\n\nAllow 90–120 days for final certification after audit submission.`;
  }

  return `I can help you navigate tax incentives for your production. Here are areas I specialize in:\n\n- **Jurisdiction comparison** — credit rates, caps, and qualification rules across states and countries\n- **Expense qualification** — which costs count toward specific incentive programs\n- **Application guidance** — documentation requirements and submission timelines\n- **Incentive stacking** — combining federal, state, and local programs effectively\n- **Budget modeling** — optimizing spend allocation for maximum incentive yield\n\nTry asking something specific — for example: *"What's the best jurisdiction for a $10M TV series?"* or *"Does VFX work done remotely qualify for the Georgia credit?"*`;
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

  function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || typing) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: trimmed, ts: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    const delay = 1400 + Math.random() * 800;
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id:      (Date.now() + 1).toString(),
        role:    'assistant',
        content: getAIResponse(trimmed),
        ts:      new Date(),
      }]);
      setTyping(false);
    }, delay);
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
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <span className="text-xs text-slate-400">Ready</span>
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

          {/* Typing indicator */}
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
