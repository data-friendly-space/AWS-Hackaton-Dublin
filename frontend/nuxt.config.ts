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
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
      awsRegion: process.env.NUXT_PUBLIC_AWS_REGION || 'us-west-2',
      awsAccessKeyId: process.env.NUXT_PUBLIC_AWS_ACCESS_KEY_ID || '',
      awsSecretAccessKey: process.env.NUXT_PUBLIC_AWS_SECRET_ACCESS_KEY || '',
    },
  },
})
