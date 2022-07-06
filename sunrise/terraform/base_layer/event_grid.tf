resource "azurerm_eventgrid_system_topic" "system_topic" {
  name                   = "eg-system-topic-${var.environment}-${var.use_case}"
  location               = var.location
  resource_group_name    = var.resource_group_name
  source_arm_resource_id = var.storage_account_id
  topic_type             = "Microsoft.Storage.StorageAccounts"

  tags = {
    env      = var.environment
    use_case = var.use_case
  }
}
