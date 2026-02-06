import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '127.0.0.1', // Force IPv4 binding
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Add port for backend
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
  },
})

