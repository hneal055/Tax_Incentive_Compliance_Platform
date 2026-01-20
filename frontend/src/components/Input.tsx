import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, className = '', id, ...props }) => {
  const inputId = id || `input-${label?.replace(/\s+/g, '-').toLowerCase()}`;
  
  return (
    <div className="w-full">
      {label && (
        <label 
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full px-4 py-3 border rounded-lg shadow-sm transition-all duration-200 
          bg-white dark:bg-gray-800 
          text-gray-900 dark:text-gray-100
          border-gray-300 dark:border-gray-600 
          focus:outline-none focus:ring-2 focus:ring-accent-blue dark:focus:ring-accent-teal 
          focus:border-transparent
          placeholder:text-gray-400 dark:placeholder:text-gray-500
          disabled:bg-gray-100 dark:disabled:bg-gray-900 disabled:cursor-not-allowed
          ${error ? 'border-status-error focus:ring-status-error' : ''} 
          ${className}`}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...props}
      />
      {error && (
        <p 
          id={`${inputId}-error`}
          className="mt-2 text-sm text-status-error dark:text-status-error flex items-center gap-1"
          role="alert"
        >
          <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;
