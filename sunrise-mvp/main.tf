terraform {
    
    required_version = ">=0.12"
    
    required_providers {
      azurerm = {
          source = "hashicorp/azurerm"
          version = "~>2.0"
      }
      random = {
        source = "hashicorp/random"
          version = "~> 3.1"
        }
    }
}

# Providers
provider azurerm {
    features {}
    subscription_id = var.subscription_id
    tenant_id = var.tenant_id
}

provider "random" {}

# Modules
module resource_group {
    source = "./resource_group"
    use_case = var.use_case
    environment = var.environment
    location = var.location
}

module storage_layer {
    source = "./storage_layer"
    use_case = var.use_case
    environment = var.environment
    resource_group_name = module.resource_group.rg_name
    location = var.location
    azad_admin_login = var.azad_admin_login
    azad_admin_object_id = var.azad_admin_object_id
}

module vault_layer {
    source = "./vault_layer"
    use_case = var.use_case
    environment = var.environment
    resource_group_name = module.resource_group.rg_name
    location = var.location
    secret_sql_admin = module.storage_layer.secret_sql_admin
    secret_sql_admin_pass = module.storage_layer.secret_sql_admin_pass
}

# module compute_layer {}

# module serve_layer {} 