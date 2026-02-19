import React from "react";
import { Link } from "react-router-dom";
import { NavLink } from "react-router-dom";

const AppHeader: React.FC = () => (
  <header className="flex items-center justify-between px-6 py-4 bg-white shadow">
    <div className="flex items-center space-x-2">
      <img src="/logo.png" alt="Logo" className="h-8 w-8" />
      <span className="font-bold text-xl">Tax Incentive Platform</span>
    </div>
    <nav className="space-x-4">
      <NavLink to="/" className="text-gray-700 hover:text-blue-600">Dashboard</NavLink>
      <NavLink to="/reports" className="text-gray-700 hover:text-blue-600">Reports</NavLink>
      <NavLink to="/settings" className="text-gray-700 hover:text-blue-600">Settings</NavLink>
    </nav>
  </header>
);

export default AppHeader;