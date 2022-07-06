# Compute transform

```hcl
module "compute_layer" {
  source                   = "./compute_layer"
  use_case                 = var.use_case
  environment              = var.environment
  resource_group_name      = module.resource_group.rg_name
  location                 = var.location
  aks_ssh_key              = var.aks_ssh_key
  aks_dns_prefix           = var.aks_dns_prefix
  azad_admin_object_id     = var.azad_admin_object_id
  service_principal_id     = var.service_principal_id
  service_principal_secret = var.service_principal_secret
}
```
