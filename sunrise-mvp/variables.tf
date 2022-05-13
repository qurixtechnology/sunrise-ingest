variable use_case {
    type = string
    description = "The use case for which the resource group will be used for."
}

variable environment {
    type = string
    description = "dev, test, prod"

    validation {
        condition = anytrue([
            var.environment == "dev",
            var.environment == "test",
            var.environment == "prod",  
        ])
        error_message = "Environment must be 'dev', 'test' or 'prod'."
    }
}

variable location {
    type = string
    description = "Azure region"
    default = "West Europe"

    validation {
        condition = anytrue([
            var.location == "West Europe",
            var.location == "Germany West Central",
            var.location == "Germany North",
            var.location == "Germany",
        ])
        error_message = "Location is not valid."
    }
    
}

variable subscription_id {
    type = string
    description = "Azure Subscription Id."
}

variable tenant_id {
    type = string
    description = "Azure tenant id."
} 

variable azad_admin_login {
    type = string
    description = "Azure AD admin login."
}

variable azad_admin_object_id {
    type = string
    description = "Azure AD admin object id."
}