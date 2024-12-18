import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  typescript: {
    // This will allow production builds to complete even with TS errors
    ignoreBuildErrors: true,
  },
  eslint: {
    // This will allow production builds to complete even with ESLint errors
    ignoreDuringBuilds: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

export default nextConfig;
