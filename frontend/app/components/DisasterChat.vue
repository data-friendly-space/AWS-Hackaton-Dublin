<script setup lang="ts">
import type { ChatMessage, SimulationScenario } from '~/types/simulation'

const props = defineProps<{
  systemSlug: string
}>()

const emit = defineEmits<{
  (e: 'scenario-generated', scenario: SimulationScenario): void
  (e: 'close'): void
}>()

const config = useRuntimeConfig()
const baseUrl = config.public.apiBase

// Chat state
const messages = ref<ChatMessage[]>([])
const input = ref('')
const isLoading = ref(false)
const error = ref<string | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)

// Suggested prompts
const suggestions = [
  'What if there\'s a drought?',
  'Simulate a disease outbreak',
  'What happens if funding is cut by 50%?',
  'Model a refugee influx scenario',
]

// Scroll to bottom when messages change
watch(messages, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}, { deep: true })

// Send message
async function sendMessage() {
  if (!input.value.trim() || isLoading.value) return

  const userMessage = input.value.trim()
  input.value = ''
  error.value = null

  // Add user message
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date(),
  })

  isLoading.value = true

  try {
    const response = await $fetch<{
      message: string
      scenario: SimulationScenario | null
      error?: string
    }>(`${baseUrl}/agents/chat/${props.systemSlug}/`, {
      method: 'POST',
      body: {
        messages: messages.value.map(m => ({
          role: m.role,
          content: m.content,
        })),
      },
    })

    if (response.error) {
      throw new Error(response.error)
    }

    // Add assistant message
    messages.value.push({
      role: 'assistant',
      content: response.message || 'No response received',
      scenario: response.scenario,
      timestamp: new Date(),
    })
  } catch (err: any) {
    error.value = err.message || 'Failed to send message'
    // Remove the failed user message
    messages.value.pop()
  } finally {
    isLoading.value = false
  }
}

// Use suggested prompt
function useSuggestion(suggestion: string) {
  input.value = suggestion
  sendMessage()
}

// Load scenario
function loadScenario(scenario: SimulationScenario) {
  emit('scenario-generated', scenario)
}

// Format message content (basic markdown-like rendering)
function formatContent(content: string | undefined | null): string {
  if (!content) return ''

  // Remove YAML blocks for display (we handle scenarios separately)
  let formatted = content.replace(/```ya?ml\n[\s\S]*?```/g, '')

  // Convert markdown-style formatting
  formatted = formatted
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 rounded">$1</code>')
    .replace(/\n/g, '<br>')

  return formatted
}
</script>

<template>
  <div class="disaster-chat flex flex-col h-full">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b">
      <div>
        <h3 class="font-semibold text-gray-900">Disaster Scenario Builder</h3>
        <p class="text-sm text-gray-500">Explore "what if" scenarios with AI</p>
      </div>
      <button
        @click="emit('close')"
        class="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Messages -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-4 space-y-4"
    >
      <!-- Welcome message if empty -->
      <div v-if="messages.length === 0" class="text-center py-8">
        <div class="text-4xl mb-4">🌍</div>
        <h4 class="font-medium text-gray-900 mb-2">Explore Disaster Scenarios</h4>
        <p class="text-sm text-gray-500 mb-4">
          Ask about potential disasters and how they might affect the health system.
          The AI will analyze the system and generate simulation scenarios.
        </p>
      </div>

      <!-- Messages -->
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="[
          'flex',
          msg.role === 'user' ? 'justify-end' : 'justify-start',
        ]"
      >
        <div
          :class="[
            'max-w-[85%] rounded-lg px-4 py-3',
            msg.role === 'user'
              ? 'bg-green-700 text-white'
              : 'bg-gray-100 text-gray-900',
          ]"
        >
          <!-- Message content -->
          <div
            class="prose prose-sm max-w-none"
            :class="msg.role === 'user' ? 'prose-invert' : ''"
            v-html="formatContent(msg.content)"
          />

          <!-- Scenario button if present -->
          <button
            v-if="msg.scenario"
            @click="loadScenario(msg.scenario)"
            class="mt-3 w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Load This Scenario
          </button>
        </div>
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading" class="flex items-center gap-2 text-gray-500">
        <div class="flex space-x-1">
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms" />
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms" />
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms" />
        </div>
        <span class="text-sm">Analyzing system impact...</span>
      </div>

      <!-- Error message -->
      <div
        v-if="error"
        class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm"
      >
        {{ error }}
      </div>
    </div>

    <!-- Input area -->
    <div class="border-t p-4">
      <!-- Suggestions -->
      <div v-if="messages.length === 0" class="flex flex-wrap gap-2 mb-3">
        <button
          v-for="suggestion in suggestions"
          :key="suggestion"
          @click="useSuggestion(suggestion)"
          class="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
        >
          {{ suggestion }}
        </button>
      </div>

      <!-- Input -->
      <div class="flex gap-2">
        <input
          v-model="input"
          type="text"
          placeholder="Describe a disaster scenario..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
          @keydown.enter="sendMessage"
          :disabled="isLoading"
        />
        <button
          @click="sendMessage"
          :disabled="!input.trim() || isLoading"
          class="px-4 py-2 bg-green-700 text-white rounded-lg hover:bg-green-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.disaster-chat {
  @apply bg-white;
}
</style>
