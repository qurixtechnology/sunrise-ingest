
resource azurerm_storage_account sa {
  name                      = "sa${var.environment}ingest${var.use_case}"
  resource_group_name       = var.resource_group_name
  location                  = var.location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  account_kind              = "StorageV2"
  allow_blob_public_access  = false
  enable_https_traffic_only = true
}

resource azurerm_app_service_plan asp {
  name                = "asp-${var.environment}-ingest-${var.use_case}"
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "functionapp"
  reserved            = true

  sku {
    size = "Y1"
    tier = "Dynamic"
  }
}

resource azurerm_application_insights appinsights {
  name                = "appi-${var.environment}-ingest-${var.use_case}"
  resource_group_name = var.resource_group_name
  location            = var.location
  application_type    = "web"
}

resource azurerm_function_app function {
  name                       = "func-${var.environment}-ingest-${var.use_case}"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  app_service_plan_id        = azurerm_app_service_plan.asp.id
  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  https_only                 = true
  os_type                    = "linux"
  version                    = "~3"

  app_settings = {
      "FUNCTIONS_WORKER_RUNTIME" = "custom"
      "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.appinsights.instrumentation_key
      # More environment variables
  }
}