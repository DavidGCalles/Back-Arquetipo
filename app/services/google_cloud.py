from google.cloud import secretmanager
from config import Config
import json

class GCPSecretManager:
    def __init__(self):
        self.project_number = Config.GCP_SETTINGS['PROJECT_NUMBER']
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id, output_type="string"):
        """
        Retrieve a secret from GCP Secret Manager.
        
        :param secret_id: ID of the secret to retrieve.
        :param version_id: Version of the secret to retrieve. Defaults to 'latest'.
        :return: The secret payload as a string.
        """
        name = self.client.secret_version_path(self.project_number, secret_id, "latest")
        response = self.client.access_secret_version(name=name)
        if output_type == "string":
            return response.payload.data.decode("UTF-8")
        elif output_type == "bytes":
            return response.payload.data
        elif output_type == "json":
            return json.loads(response.payload.data.decode("UTF-8"))