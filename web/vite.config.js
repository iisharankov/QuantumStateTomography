import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: './',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html')
      }
    }
  },
  resolve: {
    alias: {
      '@lib': resolve(__dirname, 'src/lib'),
      '@backend': resolve(__dirname, 'src/backend'),
      '@components': resolve(__dirname, 'src/components')
    }
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      // Proxy API requests to avoid CORS in development
      // The backend service runs on localhost:5000
      '/multivector': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/qml': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
});
