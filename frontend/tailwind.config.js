/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pilotforge-blue': '#2c5aa0',
        'pilotforge-green': '#28a745',
        'pilotforge-gold': '#ffc107',
      },
    },
  },
  plugins: [],
}
