RESOURCE_GROUP_NAME=rg-tf-state
STORAGE_ACCOUNT_NAME=saremotebackend
CONTAINER_NAME=dev-sunrise-state
LOCATION="westeurope"

create_remote_state_storage:
	bash create_remote_backend.sh $(RESOURCE_GROUP_NAME) \
								$(STORAGE_ACCOUNT_NAME) \
								$(CONTAINER_NAME) \
								$(LOCATION)