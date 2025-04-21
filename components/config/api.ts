// Environment-based configuration
const isProduction = process.env.NODE_ENV === 'production';

// API endpoints
export const API_ENDPOINTS = {
  BASE_URL: isProduction ? 'https://api.yourdomain.com' : 'http://localhost:8000',
  GENERATE_SCRIPT: '/api/generate-script',
  GENERATE_VIDEO: '/api/generate-video',
  AVAILABLE_STYLES: '/api/available-styles',
};

// API tokens - these should be loaded from environment variables in a real app
export const API_TOKENS = {
  HEYGEN: process.env.NEXT_PUBLIC_HEYGEN_TOKEN || 'MGQyMDA1ZjRlODZkNDMyNTg2ZDBhZWJiMDRmM2IxNTEtMTczNjExMzcxMw==', // Replace with your actual token or use env var
};

// Default avatar configuration
export const AVATAR_CONFIG = {
  DEFAULT_AVATAR: 'Anna', // Default avatar name
  QUALITY: 'high', // Default quality
};

export default {
  API_ENDPOINTS,
  API_TOKENS,
  AVATAR_CONFIG,
}; 