output secret_sql_admin {
  value = azurerm_mssql_server.sqlserver.administrator_login
}

output secret_sql_admin_pass {
  value = random_password.password.result
}