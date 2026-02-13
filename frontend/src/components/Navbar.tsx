import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Clapperboard } from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import NotificationBell from './NotificationBell';

const Navbar: React.FC = () => {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/productions', label: 'Productions' },
    { path: '/jurisdictions', label: 'Jurisdictions' },
    { path: '/calculator', label: 'Calculator' },
    { path: '/monitoring', label: 'Monitoring' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-gradient-to-r from-primary-base to-charcoal shadow-lg sticky top-0 z-40">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-accent-blue to-accent-teal rounded-lg shadow-md group-hover:shadow-lg transition-all duration-300">
              <Clapperboard className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-white text-xl font-bold tracking-tight">PilotForge</h1>
              <p className="text-blue-200 text-xs font-medium">Tax Incentive Intelligence</p>
            </div>
          </Link>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive(item.path)
                    ? 'bg-white/20 text-white shadow-sm'
                    : 'text-blue-100 hover:bg-white/10 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* Right side actions */}
          <div className="flex items-center gap-3">
            <NotificationBell />
            <ThemeToggle />
            
            {/* Mobile menu button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors focus:outline-none focus:ring-2 focus:ring-white/50"
              aria-label="Toggle menu"
              aria-expanded={isMobileMenuOpen}
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6 text-white" />
              ) : (
                <Menu className="h-6 w-6 text-white" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-white/10">
            <div className="flex flex-col gap-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={`px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    isActive(item.path)
                      ? 'bg-white/20 text-white'
                      : 'text-blue-100 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
