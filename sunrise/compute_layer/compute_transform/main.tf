resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-${var.environment}-${var.use_case}"
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.aks_dns_prefix
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name            = "agentpool"
    node_count      = 1
    vm_size         = "Standard_D2a_v4"
    type            = "VirtualMachineScaleSets"
    os_disk_size_gb = 250
  }

  service_principal {
    client_id     = var.service_principal_id
    client_secret = var.service_principal_secret
  }

  linux_profile {
    admin_username = var.aks_linux_user
    ssh_key {
      key_data = var.aks_ssh_key
    }
  }

  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "Standard"
  }

  addon_profile {
    http_application_routing {
      enabled = false
    }

    kube_dashboard {
      enabled = false
    }

    oms_agent {
      enabled = false
    }

  }
  node_resource_group = "aks-node-rg-${var.environment}-${var.use_case}"

  tags = {
    env      = var.environment
    use_case = var.use_case
  }

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [network_profile]
  }
}
