variable use_case {
    type = string
}

variable environment {
    type = string
}

variable location {
    type = string
}

variable resource_group_name {
    type = string
}

variable aks_dns_prefix {
    type = string
}

variable kubernetes_version {
    type = string
    default = "1.23.5"
}

variable aks_linux_user {
    type = string
    default = "aks_azure_user"
}

variable aks_ssh_key {
    type = string
    default = "ssh public key for AKS."
    sensitive = true 
}

variable azad_admin_object_id {
    type = string
}