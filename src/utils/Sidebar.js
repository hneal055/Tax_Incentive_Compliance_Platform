import React from 'react';

const menu = [
  { name: "Dashboard", icon: "M3 12l2-3m..." },
  { name: "Productions", icon: "M9 5H7..." },
  { name: "Jurisdictions", icon: "M9 20l-5..." },
  { name: "Calculator", icon: "M12 8c-1..." },
  { name: "Reports", icon: "M9 12l2 2 4..." },
  { name: "Settings", icon: "M10.325 4..." }
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-slate-200 shadow-sm flex flex-col">
      <div className="p-6 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-pilotforge-blue text-white">
            <span className="font-bold text-xl">⚡</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">PilotForge</h1>
            <div className="text-xs text-gray-500">Enterprise</div>
          </div>
        </div>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menu.map((item) =>
          <a
            href="#"
            key={item.name}
            className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-900 font-medium hover:bg-slate-100 transition"
          >
            <span role="img" aria-label={item.name}>{/* Icon SVG here */}</span>
            {item.name}
          </a>
        )}
      </nav>
      <div className="p-4 border-t border-slate-200">
        <div className="rounded-lg p-4 bg-slate-50">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-pilotforge-blue text-white font-bold flex items-center justify-center">
              HN
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-900 truncate">Howard Neal</div>
              <div className="text-xs text-gray-500">Admin Workspace</div>
            </div>
          </div>
          <button className="w-full py-2 rounded-lg text-sm font-medium text-gray-600 border border-slate-200 bg-white hover:bg-slate-100">
            Sign Out
          </button>
        </div>
      </div>
    </aside>
  );
}