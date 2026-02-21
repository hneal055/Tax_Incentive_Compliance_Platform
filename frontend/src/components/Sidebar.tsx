import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Clapperboard,
  Globe,
  Calculator,
  FileBarChart,
  Settings,
  LogOut,
  Zap,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/productions', label: 'Productions', icon: Clapperboard },
  { path: '/jurisdictions', label: 'Jurisdictions', icon: Globe },
  { path: '/calculator', label: 'Calculator', icon: Calculator },
  { path: '/reports', label: 'Reports', icon: FileBarChart },
  { path: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <aside
      className={`${
        collapsed ? 'w-20' : 'w-64'
      } bg-sidebar-bg flex flex-col border-r border-sidebar-border transition-all duration-300 relative`}
      role="navigation"
      aria-label="Main navigation"
    >
      {/* Collapse toggle */}
      <button
        type="button"
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-20 z-10 flex h-6 w-6 items-center justify-center rounded-full bg-accent-blue text-white shadow-lg hover:bg-accent-blue/90 transition-colors"
        aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        {collapsed ? (
          <ChevronRight className="h-3.5 w-3.5" />
        ) : (
          <ChevronLeft className="h-3.5 w-3.5" />
        )}
      </button>

      {/* Brand header */}
      <div className="flex items-center gap-3 px-5 py-5 border-b border-sidebar-border">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-accent-blue to-accent-teal shadow-md">
          <Zap className="h-5 w-5 text-white" />
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <h1 className="text-lg font-bold text-white leading-tight truncate">
              PilotForge
            </h1>
            <p className="text-[11px] text-sidebar-text leading-tight">
              Enterprise
            </p>
          </div>
        )}
      </div>

      {/* Navigation links */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {!collapsed && (
          <p className="px-3 mb-2 text-[10px] font-semibold uppercase tracking-widest text-sidebar-text/60">
            Menu
          </p>
        )}
        {navItems.map((item) => {
          const active = isActive(item.path);
          return (
            <Link
              key={item.path}
              to={item.path}
              title={collapsed ? item.label : undefined}
              className={`sidebar-nav-item flex items-center gap-3 rounded-lg font-medium text-sm
                ${collapsed ? 'justify-center px-3 py-3' : 'px-4 py-2.5'}
                ${
                  active
                    ? 'bg-sidebar-active text-sidebar-text-active shadow-sm'
                    : 'text-sidebar-text hover:bg-sidebar-hover hover:text-white'
                }
              `}
              aria-current={active ? 'page' : undefined}
            >
              <item.icon
                className={`h-5 w-5 shrink-0 ${
                  active ? 'text-accent-blue' : ''
                }`}
              />
              {!collapsed && <span>{item.label}</span>}
              {active && !collapsed && (
                <span className="ml-auto h-1.5 w-1.5 rounded-full bg-accent-blue" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User profile / sign-out */}
      <div className="border-t border-sidebar-border p-3">
        <div
          className={`rounded-lg bg-sidebar-hover p-3 ${
            collapsed ? 'flex justify-center' : ''
          }`}
        >
          <div className={`flex items-center ${collapsed ? '' : 'gap-3 mb-3'}`}>
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent-blue text-white font-bold text-sm">
              HN
            </div>
            {!collapsed && (
              <div className="overflow-hidden">
                <p className="text-sm font-semibold text-white truncate">
                  Howard Neal
                </p>
                <p className="text-[11px] text-sidebar-text">
                  Admin Workspace
                </p>
              </div>
            )}
          </div>
          {!collapsed && (
            <button
              type="button"
              className="mt-2 flex w-full items-center justify-center gap-2 rounded-lg border border-sidebar-border bg-sidebar-bg px-3 py-2 text-sm font-medium text-sidebar-text hover:bg-sidebar-hover hover:text-white transition-colors"
              aria-label="Sign out"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
