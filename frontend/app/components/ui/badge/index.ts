import { type VariantProps, cva } from 'class-variance-authority'

export { default as Badge } from './Badge.vue'

export const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        outline: 'text-foreground',
        // R4S Actor type variants
        'service-user':
          'border-actor-service-user bg-actor-service-user/10 text-actor-service-user',
        'service-provider':
          'border-actor-service-provider bg-actor-service-provider/10 text-actor-service-provider',
        support:
          'border-actor-support bg-actor-support/10 text-actor-support',
        regulatory:
          'border-actor-regulatory bg-actor-regulatory/10 text-actor-regulatory',
        // Quality variants
        good: 'border-quality-good bg-quality-good/10 text-quality-good',
        stressed: 'border-quality-stressed bg-quality-stressed/10 text-quality-stressed',
        bad: 'border-quality-bad bg-quality-bad/10 text-quality-bad',
        absent: 'border-quality-absent bg-quality-absent/10 text-quality-absent',
        // Vulnerability variants
        minimal: 'border-transparent bg-vulnerability-minimal text-white',
        low: 'border-transparent bg-vulnerability-low text-white',
        medium: 'border-transparent bg-vulnerability-medium text-white',
        high: 'border-transparent bg-vulnerability-high text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

export type BadgeVariants = VariantProps<typeof badgeVariants>
