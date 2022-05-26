#!/bin/bash

RESOURCE_GROUP_NAME=$1
STORAGE_ACCOUNT_NAME=$2
CONTAINER_NAME=$3
LOCATION="westeurope"

# Create resource group
if [ $(az group exists --name $RESOURCE_GROUP_NAME) = false ]; then
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION
fi

# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS

# Create blob container for remote backend
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME

# Get storage key

ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOUCE_GROUP_NAME --account-name=$STORAGE_ACCOUNT_NAME)
echo $ACCOUNT_KEY