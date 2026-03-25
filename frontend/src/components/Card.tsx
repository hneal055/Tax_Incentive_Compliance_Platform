import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
  footer?: React.ReactNode;
  hoverable?: boolean;
  loading?: boolean;
}

const Card: React.FC<CardProps> = ({ 
  title, 
  subtitle, 
  children, 
  className = '', 
  footer,
  hoverable = false,
  loading = false,
}) => {
  const cardContent = (
    <div className={`bg-white rounded-2xl shadow-sm overflow-hidden border border-slate-100 transition-shadow duration-200 ${hoverable ? 'hover:shadow-md' : ''} ${className}`}>
      {(title || subtitle) && (
        <div className="px-6 py-4 border-b border-slate-100">
          {title && <h3 className="text-base font-semibold text-slate-900">{title}</h3>}
          {subtitle && <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>}
        </div>
      )}
      <div className="px-6 py-4">
        {loading ? (
          <div className="animate-pulse space-y-3">
            <div className="h-4 bg-slate-200 rounded w-3/4" />
            <div className="h-4 bg-slate-200 rounded w-1/2" />
            <div className="h-4 bg-slate-200 rounded w-5/6" />
          </div>
        ) : (
          children
        )}
      </div>
      {footer && (
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-100">
          {footer}
        </div>
      )}
    </div>
  );

  if (hoverable) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {cardContent}
      </motion.div>
    );
  }

  return cardContent;
};

export default Card;
