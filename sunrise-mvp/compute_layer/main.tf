data "azuread_client_config" "current" {}

resource azuread_application aks_app {
    display_name = "sp-aks-${var.environment}-${var.use_case}-manager"
    owners =  [data.azuread_client_config.current.object_id, var.azad_admin_object_id]
}   

resource azuread_service_principal aks_sp {
  application_id               = azuread_application.aks_app.application_id
  app_role_assignment_required = false
  owners                       = [data.azuread_client_config.current.object_id, var.azad_admin_object_id]
}

resource azuread_service_principal_password aks_sp_password {
    service_principal_id = azuread_service_principal.aks_sp.object_id
}

resource azurerm_kubernetes_cluster aks {

    name = "aks-${var.environment}-${var.use_case}"
    location = var.location
    resource_group_name = var.resource_group_name
    dns_prefix = var.aks_dns_prefix
    kubernetes_version = var.kubernetes_version

    default_node_pool {
        name = "agentpool"
        node_count = 1
        vm_size = "Standard_E4s_v3"
        type = "VirtualMachineScaleSets"
        os_disk_size_gb = 250
    }

    service_principal {
        client_id = azuread_service_principal.aks_sp.application_id 
        client_secret = azuread_service_principal_password.aks_sp_password.value
    }

    linux_profile {
        admin_username = var.aks_linux_user
        ssh_key {
            key_data = var.aks_ssh_key
        }
    }

    network_profile {
        network_plugin = "kubenet"
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
    
    tags = {
        env = var.environment
        use_case = var.use_case
    } 

}