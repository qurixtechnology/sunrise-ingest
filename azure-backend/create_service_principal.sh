#!/bin/bash

SERVICE_PRINCIPAL_NAME=$1
SUBSCRIPTION_ID=$2

SERVICE_PRINCIPAL_JSON=$(az ad sp create-for-rbac --skip-assignment --name $SERVICE_PRINCIPAL_NAME -o json)
# appId
SERVICE_PRINCIPAL_ID=$(echo $SERVICE_PRINCIPAL_JSON | jq -r '.appId')
# password
SERVICE_PRINCIPAL_SECRET=$(echo $SERVICE_PRINCIPAL_JSON | jq -r '.password')

# do assignment
az role assignment create --assignee $SERVICE_PRINCIPAL_ID \
    --scope "subscriptions/$SUBSCRIPTION_ID" \
    --role Contributor

echo $SERVICE_PRINCIPAL_JSON