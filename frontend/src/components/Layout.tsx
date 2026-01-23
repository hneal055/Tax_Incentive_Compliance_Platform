import React from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-gradient-to-r from-primary-base to-charcoal text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm font-medium">
            © 2025-2026 PilotForge - Tax Incentive Intelligence for Film & TV
          </p>
          <p className="text-xs text-blue-200 mt-1">
            Powered by modern data technology
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
