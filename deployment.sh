#!/bin/bash

# ==== CONFIGURATION ====
PROJECT_ID="fourth-scheme-461516-n2"
SA_NAME="github-actions-sa"
SA_DISPLAY_NAME="GitHub Actions CI/CD"
KEY_FILE="key.json"

# ==== 1. Set project ====
echo "Setting project to $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# ==== 2. Create service account ====
echo "Creating service account: $SA_NAME"
gcloud iam service-accounts create "$SA_NAME" \
  --display-name "$SA_DISPLAY_NAME"

# ==== 3. Grant roles to the service account ====
echo "Granting roles/container.developer..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/container.developer"

echo "Granting roles/artifactregistry.writer..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# ==== 4. Generate service account key ====
echo "Creating service account key: $KEY_FILE"
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo ""
echo "✅ Service account created and key saved to $KEY_FILE"
echo "👉 Upload the contents of $KEY_FILE as a GitHub secret named: GCP_SA_KEY"
