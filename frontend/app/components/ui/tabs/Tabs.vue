<script setup lang="ts">
import { TabsRoot } from 'radix-vue'

const props = defineProps<{
  defaultValue?: string
  modelValue?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

function onValueChange(value: string) {
  emit('update:modelValue', value)
}
</script>

<template>
  <TabsRoot
    :default-value="defaultValue"
    :model-value="modelValue"
    @update:model-value="onValueChange"
  >
    <slot />
  </TabsRoot>
</template>
