// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    'shadcn-nuxt',
  ],

  shadcn: {
    prefix: '',
    componentDir: './app/components/ui',
  },

  tailwindcss: {
    cssPath: ['~/assets/css/main.css', { injectPosition: 'first' }],
    configPath: 'tailwind.config.ts',
  },

  runtimeConfig: {
    public: {
      // Use relative path so API calls go through CloudFront (which proxies to ALB)
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
    },
  },

  // Pre-render upload pages for each system
  nitro: {
    prerender: {
      routes: [
        '/systems/rmncah-eastern-ethiopia/upload',
        '/systems/wash-system-zimbabwe/upload',
        '/systems/market-system-south-sudan/upload',
      ],
    },
  },
})
