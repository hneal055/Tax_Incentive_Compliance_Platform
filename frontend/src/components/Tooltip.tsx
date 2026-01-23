import React, { useState } from 'react';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

const Tooltip: React.FC<TooltipProps> = ({ content, children, position = 'top' }) => {
  const [isVisible, setIsVisible] = useState(false);

  const getPositionClasses = () => {
    switch (position) {
      case 'top':
        return 'bottom-full left-1/2 -translate-x-1/2 mb-2';
      case 'bottom':
        return 'top-full left-1/2 -translate-x-1/2 mt-2';
      case 'left':
        return 'right-full top-1/2 -translate-y-1/2 mr-2';
      case 'right':
        return 'left-full top-1/2 -translate-y-1/2 ml-2';
    }
  };

  const getArrowClasses = () => {
    switch (position) {
      case 'top':
        return 'top-full left-1/2 -translate-x-1/2 -mt-1';
      case 'bottom':
        return 'bottom-full left-1/2 -translate-x-1/2 -mb-1';
      case 'left':
        return 'left-full top-1/2 -translate-y-1/2 -ml-1';
      case 'right':
        return 'right-full top-1/2 -translate-y-1/2 -mr-1';
    }
  };

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
      >
        {children}
      </div>
      {isVisible && (
        <div
          className={`absolute z-50 px-3 py-2 text-sm font-medium text-white bg-gray-900 dark:bg-gray-700 rounded-lg shadow-lg whitespace-nowrap animate-fade-in ${getPositionClasses()}`}
          role="tooltip"
        >
          {content}
          <div
            className={`absolute w-2 h-2 bg-gray-900 dark:bg-gray-700 transform rotate-45 ${getArrowClasses()}`}
          />
        </div>
      )}
    </div>
  );
};

export default Tooltip;
