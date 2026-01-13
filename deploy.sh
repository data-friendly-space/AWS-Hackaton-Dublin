#!/bin/bash
set -e

# Resilio Deployment Script
# Usage: ./deploy.sh [backend|frontend|all]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="${AWS_PROFILE:-resilio}"

echo "=========================================="
echo "Resilio Deployment"
echo "=========================================="
echo "AWS Profile: $PROFILE"
echo ""

# Check AWS credentials
if ! aws sts get-caller-identity --profile "$PROFILE" &>/dev/null; then
    echo "Error: AWS credentials not configured or expired"
    echo "Please run: aws configure --profile $PROFILE"
    exit 1
fi

deploy_infra() {
    echo "Deploying infrastructure with CDK..."
    cd "$SCRIPT_DIR/infra"

    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        npm install
    fi

    # Build TypeScript
    npm run build

    # Bootstrap CDK (if first time)
    npx cdk bootstrap --profile "$PROFILE" 2>/dev/null || true

    # Deploy
    npx cdk deploy --profile "$PROFILE" --require-approval never --outputs-file outputs.json

    echo "Infrastructure deployed successfully!"
    echo ""
    cat outputs.json
}

deploy_frontend() {
    echo "Building and deploying frontend..."
    cd "$SCRIPT_DIR/frontend"

    # Get outputs from CDK
    if [ ! -f "$SCRIPT_DIR/infra/outputs.json" ]; then
        echo "Error: CDK outputs not found. Run './deploy.sh infra' first."
        exit 1
    fi

    BUCKET_NAME=$(jq -r '.ResilioStack.FrontendBucketName' "$SCRIPT_DIR/infra/outputs.json")
    DISTRIBUTION_ID=$(jq -r '.ResilioStack.CloudFrontDistributionId' "$SCRIPT_DIR/infra/outputs.json")
    API_URL=$(jq -r '.ResilioStack.CloudFrontUrl' "$SCRIPT_DIR/infra/outputs.json")

    # Build frontend with API URL
    echo "Building frontend with API URL: $API_URL"
    NUXT_PUBLIC_API_BASE="$API_URL/api" npm run generate

    # Sync to S3
    echo "Uploading to S3: $BUCKET_NAME"
    aws s3 sync .output/public "s3://$BUCKET_NAME" --delete --profile "$PROFILE"

    # Invalidate CloudFront cache
    echo "Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id "$DISTRIBUTION_ID" \
        --paths "/*" \
        --profile "$PROFILE" \
        --output text

    echo "Frontend deployed successfully!"
    echo "URL: $API_URL"
}

run_migrations() {
    echo "Running database migrations..."

    # Get the ECS cluster and service names
    CLUSTER=$(aws ecs list-clusters --profile "$PROFILE" --query 'clusterArns[0]' --output text | xargs basename)
    SERVICE=$(aws ecs list-services --cluster "$CLUSTER" --profile "$PROFILE" --query 'serviceArns[0]' --output text | xargs basename)

    # Run migration task
    TASK_DEF=$(aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --profile "$PROFILE" --query 'services[0].taskDefinition' --output text)

    echo "Running migration task..."
    aws ecs run-task \
        --cluster "$CLUSTER" \
        --task-definition "$TASK_DEF" \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$(aws ec2 describe-subnets --filters Name=tag:Name,Values='*Private*' --profile "$PROFILE" --query 'Subnets[0].SubnetId' --output text)],securityGroups=[$(aws ec2 describe-security-groups --filters Name=group-name,Values='*BackendService*' --profile "$PROFILE" --query 'SecurityGroups[0].GroupId' --output text)],assignPublicIp=DISABLED}" \
        --overrides '{"containerOverrides":[{"name":"web","command":["python","manage.py","migrate"]}]}' \
        --profile "$PROFILE"

    echo "Migration task started!"
}

case "${1:-all}" in
    infra)
        deploy_infra
        ;;
    frontend)
        deploy_frontend
        ;;
    migrate)
        run_migrations
        ;;
    all)
        deploy_infra
        echo ""
        echo "Waiting for infrastructure to stabilize..."
        sleep 30
        run_migrations
        echo ""
        deploy_frontend
        ;;
    *)
        echo "Usage: $0 [infra|frontend|migrate|all]"
        echo ""
        echo "  infra    - Deploy AWS infrastructure (VPC, RDS, ECS, S3, CloudFront)"
        echo "  frontend - Build and deploy frontend to S3/CloudFront"
        echo "  migrate  - Run database migrations"
        echo "  all      - Deploy everything (default)"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
