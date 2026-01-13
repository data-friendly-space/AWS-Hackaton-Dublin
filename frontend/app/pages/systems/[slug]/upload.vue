<script setup lang="ts">
import { ArrowLeft, Upload, File, X, CheckCircle, AlertCircle, Loader2, FolderOpen, LogIn } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

const route = useRoute()
const slug = route.params.slug as string

const { getSystemBySlug } = useMockSystems()
const system = getSystemBySlug(slug)

// Auth check - only Superadmins and R4S Managers can upload
const { isAuthenticated, isSuperadmin, isR4SManager } = useAuth()
const canUpload = computed(() => isSuperadmin.value || isR4SManager.value)

useHead({
  title: () => system ? `Upload Data - ${system.name} - Resilio` : 'Upload Data',
})

// File upload state
interface UploadFile {
  id: string
  file: File
  name: string
  size: number
  progress: number
  status: 'pending' | 'uploading' | 'success' | 'error'
  error?: string
}

const files = ref<UploadFile[]>([])
const isDragging = ref(false)
const isUploading = ref(false)
const uploadComplete = ref(false)

// S3 upload composable
const { uploadFile: s3Upload, ensureFolder, bucket: S3_BUCKET, region: S3_REGION } = useS3Upload()

function generateId(): string {
  return Math.random().toString(36).substring(2, 15)
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function handleDragOver(e: DragEvent) {
  e.preventDefault()
  isDragging.value = true
}

function handleDragLeave(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false

  const droppedFiles = e.dataTransfer?.files
  if (droppedFiles) {
    addFiles(droppedFiles)
  }
}

function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) {
    addFiles(input.files)
  }
  input.value = '' // Reset input
}

function addFiles(fileList: FileList) {
  for (let i = 0; i < fileList.length; i++) {
    const file = fileList[i]
    // Check if file already exists
    if (!files.value.some(f => f.name === file.name && f.size === file.size)) {
      files.value.push({
        id: generateId(),
        file: file,
        name: file.name,
        size: file.size,
        progress: 0,
        status: 'pending'
      })
    }
  }
}

function removeFile(id: string) {
  files.value = files.value.filter(f => f.id !== id)
}

function clearAll() {
  files.value = []
  uploadComplete.value = false
}

async function uploadFiles() {
  if (files.value.length === 0 || isUploading.value) return

  isUploading.value = true
  uploadComplete.value = false

  // Get the folder name from the system slug
  const folderName = slug

  for (const uploadFile of files.value) {
    if (uploadFile.status === 'success') continue

    uploadFile.status = 'uploading'
    uploadFile.progress = 0

    try {
      // Upload to S3 folder
      await uploadToS3(uploadFile, folderName)

      uploadFile.status = 'success'
      uploadFile.progress = 100
    } catch (error: any) {
      uploadFile.status = 'error'
      uploadFile.error = error.message || 'Upload failed'
      console.error('Upload error:', error)
    }
  }

  isUploading.value = false
  uploadComplete.value = files.value.every(f => f.status === 'success')
}

async function uploadToS3(uploadFile: UploadFile, folderName: string): Promise<void> {
  // Use the S3 composable to upload via pre-signed URL
  await s3Upload(
    uploadFile.file,
    folderName,
    (progress) => {
      uploadFile.progress = progress.percentage
    }
  )
}

const totalSize = computed(() => {
  return files.value.reduce((acc, f) => acc + f.size, 0)
})

const uploadedCount = computed(() => {
  return files.value.filter(f => f.status === 'success').length
})

const hasErrors = computed(() => {
  return files.value.some(f => f.status === 'error')
})
</script>

<template>
  <div class="container py-8">
    <div v-if="!system" class="text-center py-16">
      <p class="text-destructive">System not found</p>
      <Button variant="outline" class="mt-4" as-child>
        <NuxtLink to="/systems">
          <ArrowLeft class="mr-2 h-4 w-4" />
          Back to Systems
        </NuxtLink>
      </Button>
    </div>

    <template v-else>
      <!-- Authentication Required -->
      <Alert v-if="!isAuthenticated" class="mb-8" variant="destructive">
        <LogIn class="h-4 w-4" />
        <AlertTitle>Authentication Required</AlertTitle>
        <AlertDescription>
          You must be logged in to upload files. Please log in to continue.
        </AlertDescription>
        <Button variant="outline" size="sm" class="mt-4" as-child>
          <NuxtLink to="/login">
            <LogIn class="mr-2 h-4 w-4" />
            Log In
          </NuxtLink>
        </Button>
      </Alert>

      <!-- Authorization Required - user is logged in but doesn't have permission -->
      <Alert v-else-if="!canUpload" class="mb-8" variant="destructive">
        <AlertCircle class="h-4 w-4" />
        <AlertTitle>Access Denied</AlertTitle>
        <AlertDescription>
          You do not have permission to upload files. Only Superadmins and assigned R4S Managers can upload data to systems.
        </AlertDescription>
        <Button variant="outline" size="sm" class="mt-4" as-child>
          <NuxtLink :to="`/systems/${slug}`">
            <ArrowLeft class="mr-2 h-4 w-4" />
            Back to System
          </NuxtLink>
        </Button>
      </Alert>

      <!-- Header -->
      <div class="mb-8">
        <NuxtLink :to="`/systems/${slug}`" class="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4">
          <ArrowLeft class="mr-1 h-4 w-4" />
          Back to {{ system.name }}
        </NuxtLink>

        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold text-goal-dark">Upload Data</h1>
            <p class="text-muted-foreground mt-1">
              Upload files to the <strong>{{ system.name }}</strong> data folder
            </p>
          </div>
        </div>
      </div>

      <!-- Upload Info (only visible when authenticated and authorized) -->
      <template v-if="isAuthenticated && canUpload">
        <Card class="mb-6">
          <CardContent class="pt-6">
            <div class="flex items-center gap-4">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-goal/10">
                <FolderOpen class="h-6 w-6 text-goal" />
              </div>
              <div>
                <p class="font-medium">Target Location</p>
                <p class="text-sm text-muted-foreground">
                  <code class="bg-muted px-2 py-0.5 rounded">s3://{{ S3_BUCKET }}/{{ slug }}/</code>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

      <!-- Drop Zone -->
      <Card class="mb-6">
        <CardHeader>
          <CardTitle>Select Files</CardTitle>
          <CardDescription>
            Drag and drop files or click to browse. All files will be uploaded to the system's data folder.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            :class="[
              'border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer',
              isDragging ? 'border-goal bg-goal/5' : 'border-muted-foreground/25 hover:border-goal/50 hover:bg-muted/50'
            ]"
            @dragover="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
            @click="($refs.fileInput as HTMLInputElement)?.click()"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              class="hidden"
              @change="handleFileSelect"
            />
            <Upload :class="['h-12 w-12 mx-auto mb-4', isDragging ? 'text-goal' : 'text-muted-foreground']" />
            <p class="text-lg font-medium mb-1">
              {{ isDragging ? 'Drop files here' : 'Drag & drop files here' }}
            </p>
            <p class="text-sm text-muted-foreground">
              or click to browse your computer
            </p>
          </div>
        </CardContent>
      </Card>

      <!-- File List -->
      <Card v-if="files.length > 0" class="mb-6">
        <CardHeader>
          <div class="flex items-center justify-between">
            <div>
              <CardTitle>Files to Upload ({{ files.length }})</CardTitle>
              <CardDescription>
                Total size: {{ formatFileSize(totalSize) }}
              </CardDescription>
            </div>
            <Button variant="ghost" size="sm" @click="clearAll" :disabled="isUploading">
              Clear All
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div class="space-y-3">
            <div
              v-for="file in files"
              :key="file.id"
              class="flex items-center gap-4 p-3 rounded-lg border bg-background"
            >
              <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                <File class="h-5 w-5 text-muted-foreground" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-sm truncate">{{ file.name }}</p>
                <p class="text-xs text-muted-foreground">{{ formatFileSize(file.size) }}</p>
                <Progress
                  v-if="file.status === 'uploading'"
                  :model-value="file.progress"
                  class="h-1 mt-2"
                />
              </div>
              <div class="flex items-center gap-2">
                <Badge
                  v-if="file.status === 'pending'"
                  variant="secondary"
                >
                  Pending
                </Badge>
                <Badge
                  v-else-if="file.status === 'uploading'"
                  variant="default"
                  class="bg-blue-500"
                >
                  <Loader2 class="h-3 w-3 mr-1 animate-spin" />
                  {{ file.progress }}%
                </Badge>
                <Badge
                  v-else-if="file.status === 'success'"
                  variant="default"
                  class="bg-green-500"
                >
                  <CheckCircle class="h-3 w-3 mr-1" />
                  Uploaded
                </Badge>
                <Badge
                  v-else-if="file.status === 'error'"
                  variant="destructive"
                >
                  <AlertCircle class="h-3 w-3 mr-1" />
                  Failed
                </Badge>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8"
                  @click="removeFile(file.id)"
                  :disabled="isUploading"
                >
                  <X class="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Upload Actions -->
      <div class="flex items-center justify-between">
        <div>
          <p v-if="uploadComplete" class="text-sm text-green-600 flex items-center gap-2">
            <CheckCircle class="h-4 w-4" />
            All files uploaded successfully!
          </p>
          <p v-else-if="hasErrors" class="text-sm text-destructive flex items-center gap-2">
            <AlertCircle class="h-4 w-4" />
            Some files failed to upload. Please try again.
          </p>
        </div>
        <div class="flex gap-2">
          <Button variant="outline" as-child>
            <NuxtLink :to="`/systems/${slug}`">
              Cancel
            </NuxtLink>
          </Button>
          <Button
            @click="uploadFiles"
            :disabled="files.length === 0 || isUploading"
          >
            <template v-if="isUploading">
              <Loader2 class="mr-2 h-4 w-4 animate-spin" />
              Uploading... ({{ uploadedCount }}/{{ files.length }})
            </template>
            <template v-else>
              <Upload class="mr-2 h-4 w-4" />
              Upload {{ files.length }} File{{ files.length !== 1 ? 's' : '' }}
            </template>
          </Button>
        </div>
      </div>
      </template>
    </template>
  </div>
</template>
