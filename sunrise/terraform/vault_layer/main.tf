data "azurerm_client_config" "current_client" {}

resource "azurerm_key_vault" "kv" {
  name                       = "kv-${var.environment}-${var.use_case}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current_client.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "premium"

  access_policy {
    tenant_id = data.azurerm_client_config.current_client.tenant_id
    object_id = data.azurerm_client_config.current_client.object_id

    key_permissions = [
      "create",
      "get",
    ]

    secret_permissions = [
      "set",
      "get",
      "delete",
      "list",
      "purge",
      "recover"
    ]
  }
}

resource "azurerm_key_vault_secret" "secret_sql_admin" {
  depends_on   = [azurerm_key_vault.kv]
  name         = "secret-${var.environment}-${var.use_case}-mssql-admin"
  value        = var.secret_sql_admin
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "secret_sql_admin_pass" {
  depends_on   = [azurerm_key_vault.kv]
  name         = "secret-${var.environment}-${var.use_case}-mssql-admin-pass"
  value        = var.secret_sql_admin_pass
  key_vault_id = azurerm_key_vault.kv.id
}