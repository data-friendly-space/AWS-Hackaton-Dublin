<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div
    :class="cn('rounded-xl border-2 border-gray-300 bg-white text-card-foreground shadow-md', props.class)"
  >
    <slot />
  </div>
</template>
