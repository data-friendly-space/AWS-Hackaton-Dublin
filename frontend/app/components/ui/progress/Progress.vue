<script setup lang="ts">
import { type HTMLAttributes, computed } from 'vue'
import { ProgressRoot, ProgressIndicator } from 'radix-vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  modelValue?: number
  max?: number
  class?: HTMLAttributes['class']
}>()

const percentage = computed(() => {
  const value = props.modelValue ?? 0
  const max = props.max ?? 100
  return Math.min(100, Math.max(0, (value / max) * 100))
})
</script>

<template>
  <ProgressRoot
    :model-value="props.modelValue"
    :max="props.max"
    :class="cn(
      'relative h-4 w-full overflow-hidden rounded-full bg-secondary',
      props.class
    )"
  >
    <ProgressIndicator
      class="h-full w-full flex-1 bg-goal transition-all"
      :style="`transform: translateX(-${100 - percentage}%)`"
    />
  </ProgressRoot>
</template>
