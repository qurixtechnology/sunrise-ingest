# Azure Remote Backend

## Steps

1. Create a service principal with `create_service_principal.sh`.
2. Create a remote backend with `create_remote_backend.sh`. This will
   1. Create a Azure Storage Account
   2. Create a blob container for the Terraform state file.
