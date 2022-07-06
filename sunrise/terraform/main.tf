terraform {

  required_version = ">=0.13"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.1"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~>2.22.0"
    }
  }

  backend "azurerm" {
    key = "terraform.tfstate"
  }
}

# Providers
provider "azurerm" {
  features {}
  client_id       = var.service_principal_id
  client_secret   = var.service_principal_secret
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

provider "random" {}

provider "azuread" {
  tenant_id = var.tenant_id
}

# Modules
module "resource_group" {
  source      = "./resource_group"
  use_case    = var.use_case
  environment = var.environment
  location    = var.location
}

module "storage_layer" {
  source               = "./storage_layer"
  use_case             = var.use_case
  environment          = var.environment
  resource_group_name  = module.resource_group.rg_name
  location             = var.location
  azad_admin_login     = var.azad_admin_login
  azad_admin_object_id = var.azad_admin_object_id
}

module "vault_layer" {
  source                = "./vault_layer"
  use_case              = var.use_case
  environment           = var.environment
  resource_group_name   = module.resource_group.rg_name
  location              = var.location
  secret_sql_admin      = module.storage_layer.secret_sql_admin
  secret_sql_admin_pass = module.storage_layer.secret_sql_admin_pass
}

module "ingest_layer" {
  source              = "./ingest_layer"
  use_case            = var.use_case
  environment         = var.environment
  resource_group_name = module.resource_group.rg_name
  location            = var.location
}

module "base_layer" {
  source              = "./base_layer"
  use_case            = var.use_case
  environment         = var.environment
  resource_group_name = module.resource_group.rg_name
  location            = var.location
  storage_account_id  = module.storage_layer.storage_account_id
}

# module compute_layer {}

# module serve_layer {}
