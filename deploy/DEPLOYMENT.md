# Deployment Guide – govt-customer-support

## Overview
This project deploys to **Azure Container Apps** via Azure Container Registry (ACR).

## Prerequisites
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
- Azure subscription with Container Apps access
- Azure Container Registry (ACR)
- Docker (for local builds)

## Manual Deployment

### 1. Build & Push Docker Image
```bash
az acr login --name $AZURE_ACR_NAME
docker build -t $AZURE_ACR_NAME.azurecr.io/govt-customer-support:latest .
docker push $AZURE_ACR_NAME.azurecr.io/govt-customer-support:latest
```

### 2. Create Container App
```bash
az containerapp create           --name govt-customer-support           --resource-group $AZURE_RESOURCE_GROUP           --environment $AZURE_CONTAINER_APP_ENV           --image $AZURE_ACR_NAME.azurecr.io/govt-customer-support:latest           --target-port 8080           --ingress external           --min-replicas 1           --max-replicas 5           --registry-server $AZURE_ACR_NAME.azurecr.io
```

### 3. Set Environment Variables
```bash
az containerapp update           --name govt-customer-support           --resource-group $AZURE_RESOURCE_GROUP           --set-env-vars             AZURE_OPENAI_ENDPOINT=<endpoint>             AZURE_OPENAI_API_KEY=<key>             AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

## CI/CD
The included GitHub Actions workflow (`.github/workflows/deploy.yml`)
automates build, push, and deploy on every push to `main` or manual trigger.

## Health Check
The container exposes `/health` on port 8080 for liveness and readiness probes.
