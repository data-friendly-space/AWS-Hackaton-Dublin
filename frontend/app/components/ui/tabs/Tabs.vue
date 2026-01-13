<script setup lang="ts">
import { TabsRoot } from 'radix-vue'

defineProps<{
  defaultValue?: string
  modelValue?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <TabsRoot v-bind="$attrs">
    <slot />
  </TabsRoot>
</template>
