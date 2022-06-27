data "azurerm_client_config" "client_db" {}

resource "random_password" "password" {
  length           = 20
  min_lower        = 5
  min_upper        = 5
  min_numeric      = 5
  min_special      = 2
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?'"
  lifecycle {
    ignore_changes = [min_lower, min_upper, min_numeric]
  }
}

resource "azurerm_mssql_server" "sqlserver" {
  name                         = "sql-${var.environment}-${var.use_case}"
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.admin_login
  administrator_login_password = random_password.password.result

  azuread_administrator {
    login_username              = var.azad_admin_login
    object_id                   = var.azad_admin_object_id
    azuread_authentication_only = "false"
  }

  tags = {
    env      = var.environment
    use_case = var.use_case
  }
}

resource "azurerm_mssql_database" "sqldatabase" {
  name                        = "db_${var.environment}_sunrise"
  server_id                   = azurerm_mssql_server.sqlserver.id
  max_size_gb                 = 4
  min_capacity                = 0.5
  auto_pause_delay_in_minutes = 60
  sku_name                    = "GP_S_Gen5_2"
  collation                   = "Latin1_General_100_CI_AI_SC_UTF8"

  tags = {
    env      = var.environment
    use_case = var.use_case
  }

}

resource "azurerm_storage_account" "datalake" {
  name                     = "dl${lookup(var.short_env, var.environment)}store"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
  access_tier              = "Hot"

  tags = {
    env      = var.environment
    use_case = var.use_case
  }

}