import { S3Client, PutObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3'

export interface UploadProgress {
  loaded: number
  total: number
  percentage: number
}

export interface S3UploadConfig {
  bucket: string
  region: string
  accessKeyId: string
  secretAccessKey: string
}

export function useS3Upload() {
  const config = useRuntimeConfig()

  const s3Config: S3UploadConfig = {
    bucket: 'dub01hackathongoal',
    region: config.public.awsRegion || 'us-west-2',
    accessKeyId: config.public.awsAccessKeyId || '',
    secretAccessKey: config.public.awsSecretAccessKey || ''
  }

  let s3Client: S3Client | null = null

  function getClient(): S3Client {
    if (!s3Client) {
      if (!s3Config.accessKeyId || !s3Config.secretAccessKey) {
        throw new Error('AWS credentials not configured. Set NUXT_PUBLIC_AWS_ACCESS_KEY_ID and NUXT_PUBLIC_AWS_SECRET_ACCESS_KEY environment variables.')
      }

      s3Client = new S3Client({
        region: s3Config.region,
        credentials: {
          accessKeyId: s3Config.accessKeyId,
          secretAccessKey: s3Config.secretAccessKey
        }
      })
    }
    return s3Client
  }

  /**
   * Check if a folder (prefix) exists in the S3 bucket
   */
  async function folderExists(folderName: string): Promise<boolean> {
    const client = getClient()

    try {
      const command = new ListObjectsV2Command({
        Bucket: s3Config.bucket,
        Prefix: `${folderName}/`,
        MaxKeys: 1
      })

      const response = await client.send(command)
      return (response.Contents?.length || 0) > 0
    } catch (error) {
      console.error('Error checking folder:', error)
      return false
    }
  }

  /**
   * Create a folder in S3 (by creating an empty object with trailing slash)
   */
  async function createFolder(folderName: string): Promise<void> {
    const client = getClient()

    const command = new PutObjectCommand({
      Bucket: s3Config.bucket,
      Key: `${folderName}/`,
      Body: ''
    })

    await client.send(command)
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
   * Upload a file to S3
   */
  async function uploadFile(
    file: File,
    folderName: string,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<string> {
    const client = getClient()
    const key = `${folderName}/${file.name}`

    // Ensure folder exists
    await ensureFolder(folderName)

    // Read file as ArrayBuffer
    const arrayBuffer = await file.arrayBuffer()
    const body = new Uint8Array(arrayBuffer)

    const command = new PutObjectCommand({
      Bucket: s3Config.bucket,
      Key: key,
      Body: body,
      ContentType: file.type || 'application/octet-stream'
    })

    // Note: The AWS SDK v3 doesn't support upload progress directly
    // For progress tracking with large files, you'd use @aws-sdk/lib-storage
    // For simplicity in this demo, we simulate progress
    if (onProgress) {
      onProgress({ loaded: 0, total: file.size, percentage: 0 })
    }

    await client.send(command)

    if (onProgress) {
      onProgress({ loaded: file.size, total: file.size, percentage: 100 })
    }

    return `s3://${s3Config.bucket}/${key}`
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

    for (let i = 0; i < files.length; i++) {
      try {
        await uploadFile(
          files[i],
          folderName,
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
    const client = getClient()

    const command = new ListObjectsV2Command({
      Bucket: s3Config.bucket,
      Prefix: `${folderName}/`
    })

    const response = await client.send(command)
    return response.Contents?.map(obj => obj.Key || '').filter(key => key !== `${folderName}/`) || []
  }

  return {
    uploadFile,
    uploadFiles,
    folderExists,
    createFolder,
    ensureFolder,
    listFiles,
    bucket: s3Config.bucket,
    region: s3Config.region
  }
}
