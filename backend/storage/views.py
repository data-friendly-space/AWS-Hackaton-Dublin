import json
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def get_s3_client():
    """Get S3 client configured with AWS credentials."""
    client_kwargs = {
        'region_name': settings.AWS_S3_REGION,
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
    }
    # Include session token if using temporary credentials
    if settings.AWS_SESSION_TOKEN:
        client_kwargs['aws_session_token'] = settings.AWS_SESSION_TOKEN
    return boto3.client('s3', **client_kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_presigned_url(request):
    """
    Generate a pre-signed URL for uploading a file to S3.

    Expected payload:
    {
        "filename": "example.pdf",
        "content_type": "application/pdf",
        "folder": "system-name"
    }
    """
    try:
        filename = request.data.get('filename')
        content_type = request.data.get('content_type', 'application/octet-stream')
        folder = request.data.get('folder', '')

        if not filename:
            return Response(
                {'error': 'filename is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construct the S3 key (path)
        if folder:
            s3_key = f"{folder}/{filename}"
        else:
            s3_key = filename

        s3_client = get_s3_client()

        # Generate pre-signed URL for PUT operation
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.AWS_S3_BUCKET,
                'Key': s3_key,
                'ContentType': content_type,
            },
            ExpiresIn=3600  # URL valid for 1 hour
        )

        return Response({
            'url': presigned_url,
            'key': s3_key,
            'bucket': settings.AWS_S3_BUCKET,
            'expires_in': 3600
        })

    except ClientError as e:
        return Response(
            {'error': f'Failed to generate pre-signed URL: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Unexpected error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_presigned_urls_batch(request):
    """
    Generate pre-signed URLs for multiple files.

    Expected payload:
    {
        "files": [
            {"filename": "file1.pdf", "content_type": "application/pdf"},
            {"filename": "file2.xlsx", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        ],
        "folder": "system-name"
    }
    """
    try:
        files = request.data.get('files', [])
        folder = request.data.get('folder', '')

        if not files:
            return Response(
                {'error': 'files array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        s3_client = get_s3_client()
        results = []

        for file_info in files:
            filename = file_info.get('filename')
            content_type = file_info.get('content_type', 'application/octet-stream')

            if not filename:
                continue

            # Construct the S3 key (path)
            if folder:
                s3_key = f"{folder}/{filename}"
            else:
                s3_key = filename

            try:
                presigned_url = s3_client.generate_presigned_url(
                    'put_object',
                    Params={
                        'Bucket': settings.AWS_S3_BUCKET,
                        'Key': s3_key,
                        'ContentType': content_type,
                    },
                    ExpiresIn=3600
                )

                results.append({
                    'filename': filename,
                    'url': presigned_url,
                    'key': s3_key,
                    'content_type': content_type
                })
            except ClientError as e:
                results.append({
                    'filename': filename,
                    'error': str(e)
                })

        return Response({
            'urls': results,
            'bucket': settings.AWS_S3_BUCKET,
            'expires_in': 3600
        })

    except Exception as e:
        return Response(
            {'error': f'Unexpected error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_folder_exists(request):
    """
    Check if a folder exists in S3.

    Query params:
    - folder: the folder name to check
    """
    try:
        folder = request.query_params.get('folder', '')

        if not folder:
            return Response(
                {'error': 'folder parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        s3_client = get_s3_client()

        # Check if any objects exist with this prefix
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=f"{folder}/",
            MaxKeys=1
        )

        exists = response.get('KeyCount', 0) > 0

        return Response({
            'folder': folder,
            'exists': exists
        })

    except ClientError as e:
        return Response(
            {'error': f'Failed to check folder: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_folder(request):
    """
    Create a folder in S3 (creates a zero-byte object with trailing slash).

    Expected payload:
    {
        "folder": "system-name"
    }
    """
    try:
        folder = request.data.get('folder', '')

        if not folder:
            return Response(
                {'error': 'folder is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        s3_client = get_s3_client()

        # Create a zero-byte object to represent the folder
        s3_client.put_object(
            Bucket=settings.AWS_S3_BUCKET,
            Key=f"{folder}/",
            Body=b''
        )

        return Response({
            'folder': folder,
            'created': True
        })

    except ClientError as e:
        return Response(
            {'error': f'Failed to create folder: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    """
    List files in a folder.

    Query params:
    - folder: the folder to list files from
    """
    try:
        folder = request.query_params.get('folder', '')

        s3_client = get_s3_client()

        prefix = f"{folder}/" if folder else ""

        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_S3_BUCKET,
            Prefix=prefix
        )

        files = []
        for obj in response.get('Contents', []):
            key = obj['Key']
            # Skip the folder marker itself
            if key != prefix:
                files.append({
                    'key': key,
                    'filename': key.replace(prefix, ''),
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
                })

        return Response({
            'folder': folder,
            'files': files,
            'count': len(files)
        })

    except ClientError as e:
        return Response(
            {'error': f'Failed to list files: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
