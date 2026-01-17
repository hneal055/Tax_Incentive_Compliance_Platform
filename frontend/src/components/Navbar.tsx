import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/productions', label: 'Productions' },
    { path: '/jurisdictions', label: 'Jurisdictions' },
    { path: '/calculator', label: 'Calculator' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-pilotforge-blue shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <span className="text-2xl">🎬</span>
            <div>
              <h1 className="text-white text-xl font-bold">PilotForge</h1>
              <p className="text-blue-200 text-xs">Tax Incentive Intelligence</p>
            </div>
          </div>
          
          <div className="flex space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive(item.path)
                    ? 'bg-blue-700 text-white'
                    : 'text-blue-100 hover:bg-blue-600 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
