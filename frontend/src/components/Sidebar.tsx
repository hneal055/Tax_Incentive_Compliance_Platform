import React, { useState } from 'react';
import { LayoutDashboard, Clapperboard, Calculator, Globe, Zap, Menu, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  label: string;
  icon: React.ReactNode;
  path: string;
  isNew?: boolean;
}

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const location = useLocation();

  const navItems: NavItem[] = [
    {
      label: 'Dashboard',
      icon: <LayoutDashboard className="w-5 h-5" />,
      path: '/dashboard',
    },
    {
      label: 'Productions',
      icon: <Clapperboard className="w-5 h-5" />,
      path: '/productions',
    },
    {
      label: 'Incentive Calculator',
      icon: <Calculator className="w-5 h-5" />,
      path: '/calculator',
    },
    {
      label: 'Jurisdictions',
      icon: <Globe className="w-5 h-5" />,
      path: '/jurisdictions',
    },
    {
      label: 'AI Advisor',
      icon: <Zap className="w-5 h-5" />,
      path: '/ai-advisor',
      isNew: true,
    },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <>
      {/* Mobile Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="md:hidden fixed top-4 left-4 z-40 p-2 bg-slate-900 text-white rounded-lg"
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white transition-all duration-300 z-30 ${
          isOpen ? 'w-64' : 'w-0'
        } md:w-64 overflow-hidden`}
      >
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center font-bold text-lg">
              $
            </div>
            <h1 className="text-xl font-bold">SceneIQ</h1>
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {navItems.map((item, idx) => (
            <Link
              key={idx}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors group ${
                isActive(item.path)
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <span className="group-hover:scale-110 transition-transform">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
              {item.isNew && (
                <span className="ml-auto text-xs bg-blue-500 px-2 py-1 rounded font-semibold">
                  NEW
                </span>
              )}
            </Link>
          ))}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-700">
          <div className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-700 cursor-pointer transition-colors">
            <div className="w-8 h-8 bg-slate-600 rounded-full flex items-center justify-center text-xs font-bold">
              FM
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">Finance Manager</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Offset */}
      <div className={`transition-all duration-300 ${isOpen ? 'md:ml-64' : ''}`} />
    </>
  );
}
