import React from 'react';

export default function Topbar() {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center shadow">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-sm text-gray-500">Welcome back, Howard. Here’s your compliance overview.</p>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-slate-50 border border-slate-200">
          <span className="w-3 h-3 rounded-full bg-status-active inline-block animate-pulse-soft" />
          <span className="text-sm font-medium text-gray-700">System Healthy</span>
        </div>
        <div className="w-10 h-10 rounded-full bg-pilotforge-blue flex items-center justify-center text-white font-bold">
          HN
        </div>
      </div>
    </header>
  );
}