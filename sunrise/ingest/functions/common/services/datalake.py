import logging
import posixpath
from pathlib import PurePosixPath
from typing import Any, List, Optional, Union

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import (
    ManagedIdentityCredential,
    AzureCliCredential,
    ChainedTokenCredential,
)
from abc import ABC, abstractclassmethod


class DataLakeClientBase(ABC):
    @abstractclassmethod
    def list_directory(self):
        raise NotImplementedError

    @abstractclassmethod
    def get_file_content(self):
        raise NotImplementedError


class DataLakeClient(DataLakeClientBase):
    """Client to interact with the Data Lake."""

    def __init__(
        self,
        container_name: Optional[str],
        connection_string: Optional[str],
        account_name: Optional[str],
    ):
        self.container_name = container_name
        self.connection_string = connection_string
        self.account_name = account_name

    @classmethod
    def create_with_connection_string(
        cls, container_name: str, connection_string: str
    ) -> DataLakeClientBase:
        client = cls(
            container_name=container_name,
            connection_string=connection_string,
            account_name=None,
        )
        client.client = DataLakeServiceClient.from_connection_string(
            conn_str=connection_string
        )
        return client

    @classmethod
    def create_with_az_aad_auth(
        cls, container_name: str, account_name: str
    ) -> DataLakeClientBase:
        client = cls(
            container_name=container_name,
            connection_string=None,
            account_name=account_name,
        )

        # Managed Identity Credential flow is used, when the function
        # is deployed to azure
        # and the managed identity of the function
        # is activated and permitted via IAM.
        managed_identity_credential = ManagedIdentityCredential()

        # Azure CLI Credential flow is used, when the managed identity is not
        # found in the current environment.
        # This means the function is running locally -->
        # use the cli credentials to allow local access to cloud resources.
        azure_cli_credential = AzureCliCredential()

        credential_chain = ChainedTokenCredential(
            managed_identity_credential, azure_cli_credential
        )

        account_url = f"https://{account_name}.dfs.core.windows.net/"

        client.container_name = container_name
        client.client = DataLakeServiceClient(
            account_url=account_url, credential=credential_chain
        )
        return client

    def list_directory(
        self,
        dir_path: str,
        files_only: bool = False,
        file_ending: str = None,
        file_starts_with: str = None,
        return_only_paths: bool = False,
    ) -> List:
        """Lists content of a directory.

        Args:
            dir_path (str): Path to the directory
            files_only (bool, optional): if true, returns only files and
            not directories.
                Defaults to False.
            file_ending (str, optional): filters on the file ending (suffix).
                Defaults to None.
            return_only_paths (bool, optional): if true returns only the paths
            to the files and directories.
                Defaults to False.

        Returns:
            List: Elements in the directory.
        """
        result = list()
        fs_client = self.client.get_file_system_client(self.container_name)
        paths = fs_client.get_paths(path=dir_path, recursive=False)

        try:
            result = []
            for item in paths:
                if files_only:
                    if item.is_directory:
                        # skip dirs
                        pass
                    else:
                        result.append(item)
                else:
                    result.append(item)

        except ResourceNotFoundError as e:
            logging.warning(e)
            logging.warning(
                f"Container: {self.container_name} Path: {dir_path}"
            )

        if file_ending is not None:
            tmp = [item for item in result if item.name.endswith(file_ending)]
            result = tmp

        if file_starts_with is not None:
            tmp = [
                item
                for item in result
                if PurePosixPath(item.name).name.startswith(file_starts_with)
            ]
            result = tmp

        if return_only_paths:
            tmp = [item.name for item in result]
            result = tmp

        return result

    def get_file_content(
        self, file_path: str, raw_content: bool = False, encoding: str = "utf-8"
    ) -> Union[str, bytes]:
        """Returns the content of a file from the Data Lake.

        Args:
            file_path (str): Path to the file.
            raw_content (bool, optional): if true returns the bytes of the file.
                Defaults to False.
            encoding (str, optional): Encoding of the file. Defaults to "utf-8".

        Returns:
            Union[str, bytes]: Content of the file.
        """
        dir_path = posixpath.split(file_path)[0]
        file_name = posixpath.split(file_path)[1]

        fs_client = self.client.get_file_system_client(self.container_name)
        dir_client = fs_client.get_directory_client(dir_path)
        file_client = dir_client.get_file_client(file_name)

        if raw_content:
            result = file_client.download_file().readall()
        else:
            result = file_client.download_file().readall().decode(encoding)
        return result

    def upload_file_content(
        self,
        content: Any,
        file_path: str = None,
        dir_path: str = None,
        file_name: str = None,
    ) -> None:
        """Uploads the given content as a new file on the Data Lake.

        Args:
            content (any): Content of the new file.
            file_path (str, optional): Path to the new file.
                Defaults to None.
            dir_path (str, optional): Directory for the new file.
                Defaults to None.
            file_name (str, optional): Name of the new file.
                Defaults to None.
        """
        if file_path is not None:
            dir_path = posixpath.split(file_path)[0]
            file_name = posixpath.split(file_path)[1]

        logging.info(f"Write file to datalake: {dir_path}/{file_name}")
        fs_client = self.client.get_file_system_client(self.container_name)
        dir_client = fs_client.get_directory_client(dir_path)
        file_client = dir_client.get_file_client(file_name)
        file_client.upload_data(content, overwrite=True)

    def copy_file(self, source_file_path: str, target_file_path: str) -> None:
        """Copys a file from a given source file path to a given target file path, bitwise.

        Args:
            source_file_path (str): Path to the file to copy-
            target_file_path (str): Path to the new file location.
        """
        logging.info(
            f"Copy file from: {source_file_path} to {target_file_path}"
        )

        source_dir_path = posixpath.split(source_file_path)[0]
        source_file_name = posixpath.split(source_file_path)[1]

        target_dir_path = posixpath.split(target_file_path)[0]
        target_file_name = posixpath.split(target_file_path)[1]

        source_fs_client = self.client.get_file_system_client(
            self.container_name
        )
        source_dir_client = source_fs_client.get_directory_client(
            source_dir_path
        )
        source_file_client = source_dir_client.get_file_client(source_file_name)

        target_fs_client = self.client.get_file_system_client(
            self.container_name
        )
        target_dir_client = target_fs_client.get_directory_client(
            target_dir_path
        )
        target_file_client = target_dir_client.get_file_client(target_file_name)

        file_content = source_file_client.download_file().readall()
        target_file_client.upload_data(file_content, overwrite=True)
