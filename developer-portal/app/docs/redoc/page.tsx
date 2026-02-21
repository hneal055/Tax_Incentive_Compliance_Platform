'use client';

import { RedocStandalone } from 'redoc';

export default function ReDocPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-full">
        <RedocStandalone
          specUrl="/openapi.json"
          options={{
            nativeScrollbars: true,
            theme: {
              colors: {
                primary: {
                  main: '#2563eb'
                }
              },
              typography: {
                fontSize: '16px',
                fontFamily: 'var(--font-geist-sans), system-ui, sans-serif',
                headings: {
                  fontFamily: 'var(--font-geist-sans), system-ui, sans-serif'
                }
              }
            }
          }}
        />
      </div>
    </div>
  );
}
