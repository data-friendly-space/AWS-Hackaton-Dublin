/**
 * S3 Upload composable using backend pre-signed URLs
 * This approach keeps AWS credentials secure on the backend
 */

export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

interface PresignedUrlResponse {
  url: string
  key: string
  bucket: string
  expires_in: number
}

interface PresignedUrlsBatchResponse {
  urls: Array<{
    filename: string
    url: string
    key: string
    content_type: string
    error?: string
  }>
  bucket: string
  expires_in: number
}

interface FolderCheckResponse {
  folder: string
  exists: boolean
}

interface FolderCreateResponse {
  folder: string
  created: boolean
}

interface FileInfo {
  key: string
  filename: string
  size: number
  last_modified: string
}

interface ListFilesResponse {
  folder: string
  files: FileInfo[]
  count: number
}

export function useS3Upload() {
  const config = useRuntimeConfig()
  const { authFetch, accessToken } = useAuth()
  const baseUrl = config.public.apiBase

  const bucket = 'dub01hackathongoal'
  const region = 'us-west-2'

  /**
   * Check if a folder exists in the S3 bucket
   */
  async function folderExists(folderName: string): Promise<boolean> {
    try {
      const response = await authFetch<FolderCheckResponse>(
        `${baseUrl}/storage/folder/check/?folder=${encodeURIComponent(folderName)}`
      )
      return response.exists
    } catch (error) {
      console.error('Error checking folder:', error)
      return false
    }
  }

  /**
   * Create a folder in S3
   */
  async function createFolder(folderName: string): Promise<void> {
    await authFetch<FolderCreateResponse>(`${baseUrl}/storage/folder/create/`, {
      method: 'POST',
      body: { folder: folderName }
    })
  }

  /**
   * Ensure folder exists, creating it if necessary
   */
  async function ensureFolder(folderName: string): Promise<void> {
    const exists = await folderExists(folderName)
    if (!exists) {
      await createFolder(folderName)
    }
  }

  /**
   * Get a pre-signed URL for a single file
   */
  async function getPresignedUrl(
    filename: string,
    contentType: string,
    folder: string
  ): Promise<PresignedUrlResponse> {
    return await authFetch<PresignedUrlResponse>(`${baseUrl}/storage/presigned-url/`, {
      method: 'POST',
      body: {
        filename,
        content_type: contentType,
        folder
      }
    })
  }

  /**
   * Get pre-signed URLs for multiple files
   */
  async function getPresignedUrlsBatch(
    files: Array<{ filename: string; content_type: string }>,
    folder: string
  ): Promise<PresignedUrlsBatchResponse> {
    return await authFetch<PresignedUrlsBatchResponse>(`${baseUrl}/storage/presigned-urls/`, {
      method: 'POST',
      body: {
        files,
        folder
      }
    })
  }

  /**
   * Upload a file using a pre-signed URL
   */
  async function uploadWithPresignedUrl(
    file: File,
    presignedUrl: string,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onProgress) {
          onProgress({
            loaded: event.loaded,
            total: event.total,
            percentage: Math.round((event.loaded / event.total) * 100)
          })
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Upload failed with status ${xhr.status}`))
        }
      })

      xhr.addEventListener('error', () => {
        reject(new Error('Upload failed due to network error'))
      })

      xhr.open('PUT', presignedUrl, true)
      xhr.setRequestHeader('Content-Type', file.type || 'application/octet-stream')
      xhr.send(file)
    })
  }

  /**
   * Upload a file to S3 (gets pre-signed URL and uploads)
   */
  async function uploadFile(
    file: File,
    folderName: string,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<string> {
    // Get pre-signed URL
    const presigned = await getPresignedUrl(
      file.name,
      file.type || 'application/octet-stream',
      folderName
    )

    // Upload using the pre-signed URL
    await uploadWithPresignedUrl(file, presigned.url, onProgress)

    return `s3://${presigned.bucket}/${presigned.key}`
  }

  /**
   * Upload multiple files to S3 with progress tracking
   */
  async function uploadFiles(
    files: File[],
    folderName: string,
    onFileProgress?: (fileIndex: number, progress: UploadProgress) => void,
    onFileComplete?: (fileIndex: number, success: boolean, error?: string) => void
  ): Promise<{ successful: number; failed: number }> {
    let successful = 0
    let failed = 0

    // Ensure folder exists before uploading
    await ensureFolder(folderName)

    // Get all pre-signed URLs at once for efficiency
    const fileInfos = files.map((file) => ({
      filename: file.name,
      content_type: file.type || 'application/octet-stream'
    }))

    const presignedResponse = await getPresignedUrlsBatch(fileInfos, folderName)

    // Upload each file using its pre-signed URL
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const presigned = presignedResponse.urls[i]

      if (presigned.error) {
        failed++
        onFileComplete?.(i, false, presigned.error)
        continue
      }

      try {
        await uploadWithPresignedUrl(
          file,
          presigned.url,
          onFileProgress ? (progress) => onFileProgress(i, progress) : undefined
        )
        successful++
        onFileComplete?.(i, true)
      } catch (error: any) {
        failed++
        onFileComplete?.(i, false, error.message)
      }
    }

    return { successful, failed }
  }

  /**
   * List files in a folder
   */
  async function listFiles(folderName: string): Promise<string[]> {
    const response = await authFetch<ListFilesResponse>(
      `${baseUrl}/storage/files/?folder=${encodeURIComponent(folderName)}`
    )
    return response.files.map((f) => f.key)
  }

  /**
   * Check if the backend storage API is configured
   */
  function isConfigured(): boolean {
    return !!accessToken.value
  }

  return {
    uploadFile,
    uploadFiles,
    folderExists,
    createFolder,
    ensureFolder,
    listFiles,
    isConfigured,
    bucket,
    region
  }
}
