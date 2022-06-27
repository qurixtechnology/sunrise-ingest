variable "use_case" {
  type        = string
  description = "The use case for which the resource group will be used for."
}

variable "environment" {
  type        = string
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

variable "short_env" {
  type = map(string)

  default = {
    dev  = "d"
    test = "t"
    prod = "p"
  }

}


variable "location" {
  type        = string
  description = "Azure region"
  default     = "West Europe"

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

variable "resource_group_name" {
  type        = string
  description = "Resource Group where the Storage resources belong to."
}

variable "admin_login" {
  type        = string
  default     = "sunriseAdmin"
  description = "Admin login (not Azure AD)."
}

variable "azad_admin_login" {
  type        = string
  description = "Azure AD admin login."
}

variable "azad_admin_object_id" {
  type        = string
  description = "Azure AD admin object id."
}

variable "db_user_names" {
  type        = list(any)
  description = "List of Azure AD user names."
  default = ["fernando.zepeda@qurix.tech",
    "martens@qurix.tech",
    "andree.deboer@qurix.tech",
    "konkevich@qurix.tech",
    "lakshmi.chittem@qurix.tech",
  ]
}