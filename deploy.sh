#!/bin/bash
# ================================================
# Cine-AI — Automated GCP Deployment Script
# Bonus: Infrastructure-as-Code for hackathon
# ================================================

set -e  # Exit on any error

PROJECT_ID="tribal-quest-490419-s4"
REGION="us-central1"
SERVICE_NAME="cine-ai"

echo "🚀 Deploying Cine-AI to Google Cloud Run..."
echo "   Project : $PROJECT_ID"
echo "   Region  : $REGION"

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "⚙️  Enabling APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com

# Deploy to Cloud Run
echo "📦 Building and deploying container..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --memory 1Gi \
  --timeout 300

echo "✅ Deployment complete!"
echo "🌐 Your app is live at the URL shown above."
