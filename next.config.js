/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@supabase/supabase-js'],
  },
  images: {
    domains: ['localhost'],
    unoptimized: true,
  },
  webpack: (config, { isServer }) => {
    // Otimizações para reduzir tamanho do bundle
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }

    // Tree shaking mais agressivo
    config.optimization = {
      ...config.optimization,
      usedExports: true,
      sideEffects: false,
    };

    return config;
  },
  // Otimizações de build
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  generateEtags: false,
  // Garantir que as APIs sejam reconhecidas
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ];
  },
}

module.exports = nextConfig
