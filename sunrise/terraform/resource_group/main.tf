resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.environment}-${var.use_case}"
  location = var.location

  tags = {
    env      = var.environment
    use_case = var.use_case
  }
}