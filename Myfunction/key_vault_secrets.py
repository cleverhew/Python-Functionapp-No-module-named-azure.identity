# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import os
import logging
import uuid
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class KeyVault:
    def __init__(self):
        # DefaultAzureCredential() expects the following environment variables:
        # * AZURE_CLIENT_ID
        # * AZURE_CLIENT_SECRET
        # * AZURE_TENANT_ID

        credential = DefaultAzureCredential()
        self.secret_client = SecretClient(
            vault_url=os.environ["AZURE_PROJECT_URL"], credential=credential
        )

        self.secret_name = "secret-name-" + uuid.uuid1().hex
        self.secret_Value = "secret-value"

    def set_secret(self):
        logging.info("Setting a secret...")
        self.secret_client.set_secret(self.secret_name, self.secret_Value)
        logging.info("\tdone")

    def get_secret(self):
        logging.info("Getting a secret...")
        secret = self.secret_client.get_secret(self.secret_name)
        logging.info("\tdone, secret: (" + secret.name + "," + secret.value + ").")

    def delete_secret(self):
        logging.info("Deleting a secret...")
        deleted_poller = self.secret_client.begin_delete_secret(self.secret_name)
        deleted_secret = deleted_poller.result()
        logging.info("\tdone: " + deleted_secret.name)

    def run(self):
        logging.info("")
        logging.info("------------------------")
        logging.info("Key Vault - Secrets\nIdentity - Credential")
        logging.info("------------------------")
        logging.info("1) Set a secret")
        logging.info("2) Get that secret")
        logging.info("3) Delete that secret (Clean up the resource)")
        logging.info("")

        try:
            self.set_secret()
            self.get_secret()
        finally:
            self.delete_secret()
