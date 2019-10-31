# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import os
import logging
import uuid
from azure.storage.blob import BlobClient
from azure.core import exceptions


class StorageBlob:
    def __init__(self):
        id = uuid.uuid1()

        connectionString = os.environ["STORAGE_CONNECTION_STRING"]
        self.blob = BlobClient.from_connection_string(
            connectionString,
            container_name="mycontainer",
            blob_name="pyTestBlob-" + id.hex + ".txt",
        )

    def upload_blob(self):
        logging.info("uploading blob...")
        self.data = "This is a sample data for Python Test"
        self.blob.upload_blob(self.data)
        logging.info("\tdone")

    def download_blob(self):
        logging.info("downloading blob...")
        with open("./downloadedBlob.txt", "wb+") as my_blob:
            my_blob.writelines([self.blob.download_blob().content_as_bytes()])

        logging.info("\tdone")

    def delete_blob(self):
        logging.info("Cleaning up the resource...")
        self.blob.delete_blob()
        logging.info("\tdone")

    def run(self):
        logging.info("")
        logging.info("------------------------")
        logging.info("Storage - Blob")
        logging.info("------------------------")
        logging.info("1) Upload a Blob")
        logging.info("2) Download a Blob")
        logging.info("3) Delete that Blob (Clean up the resource)")
        logging.info("")

        # Ensure that the blob does not exists before the tests
        try:
            self.delete_blob()
        except exceptions.AzureError:
            pass

        try:
            self.upload_blob()
            self.download_blob()
        finally:
            self.delete_blob()
