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

const API_BASE = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000') as string;
const API_VERSION = (import.meta.env.VITE_API_VERSION || '0.1.0') as string;
const TOKEN_KEY = 'pilotforge_token';

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
  // Track the current streaming abort controller so we can cancel mid-stream
  const abortRef                = useRef<AbortController | null>(null);

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

    // Snapshot history before state update for API payload
    const historyForApi = [
      ...messages.filter(m => m.id !== '0'),
      userMsg,
    ].map(m => ({ role: m.role, content: m.content }));

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    const assistantId = (Date.now() + 1).toString();
    const assistantTs = new Date();
    let content = '';
    let firstChunk = true;

    const abort = new AbortController();
    abortRef.current = abort;

    try {
      const token = localStorage.getItem(TOKEN_KEY);
      const response = await fetch(
        `${API_BASE}/api/${API_VERSION}/advisor/chat`,
        {
          method: 'POST',
          signal: abort.signal,
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify({
            messages: historyForApi,
            production_id: production !== 'none' ? production : undefined,
          }),
        }
      );

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error((err as { detail?: string }).detail ?? `HTTP ${response.status}`);
      }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        // Keep the last (potentially incomplete) line in the buffer
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const payload = line.slice(6);
          if (payload === '[DONE]') break;

          try {
            const parsed = JSON.parse(payload) as { delta?: string; error?: string };
            if (parsed.error) throw new Error(parsed.error);
            if (parsed.delta) {
              content += parsed.delta;
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
            }
          } catch (parseErr) {
            if ((parseErr as Error).message !== 'Unexpected end of JSON input') {
              throw parseErr;
            }
          }
        }
      }

      // If we never got a chunk (empty response), show a fallback
      if (firstChunk) {
        setTyping(false);
        setMessages(prev => [
          ...prev,
          { id: assistantId, role: 'assistant', content: 'No response received. Please try again.', ts: assistantTs },
        ]);
      }
    } catch (err: unknown) {
      if ((err as { name?: string }).name === 'AbortError') return;
      setTyping(false);
      const detail = err instanceof Error ? err.message : 'Unknown error';
      const errorContent =
        detail.includes('not configured') || detail.includes('503')
          ? 'AI Advisor is currently unavailable — the service is not configured on the server.'
          : detail.includes('credit balance') || detail.includes('billing') || detail.includes('402')
          ? 'AI Advisor is temporarily unavailable. Please contact your administrator to resolve the service configuration.'
          : `Sorry, I encountered an error: ${detail}. Please try again.`;
      setMessages(prev => [
        ...prev,
        { id: assistantId, role: 'assistant', content: errorContent, ts: assistantTs },
      ]);
    } finally {
      abortRef.current = null;
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  function handleClear() {
    abortRef.current?.abort();
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
