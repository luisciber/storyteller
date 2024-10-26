from io import BytesIO

from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

from app.core.config import settings


class BucketService:
    def __init__(self):
        if settings.development:
            self.storage_client = storage.Client(
                project=settings.gcp_project_id,
                credentials=AnonymousCredentials(),
                client_options={"api_endpoint": settings.bucket_url}
            )
        else:
            self.storage_client = storage.Client(
                project=settings.gcp_project_id
            )

        self.bucket_name = settings.bucket_name
        self.bucket = self.storage_client.bucket(self.bucket_name)

    async def upload_file(self, data: bytes, path: str, content_type: str = "image/webp"):
        """Sube un archivo al bucket."""
        blob = self.bucket.blob(path)

        # Subir el contenido al blob
        file_obj = BytesIO(data)
        blob.upload_from_file(file_obj, content_type=content_type, rewind=True)

        # if not settings.development:
        #     blob.make_public()

        return blob.public_url

    def delete_file(self, blob_name: str):
        """Elimina un archivo del bucket."""
        blob = self.bucket.blob(blob_name)
        blob.delete()

    def get_file_url(self, path: str):
        """Obtiene la URL de un archivo en el bucket."""
        return self.bucket.blob(path).public_url

    def list_bucket_elements(self):
        """Listar los elementos del bucket."""
        blobs = self.bucket.list_blobs()

        # Crear una lista con los nombres de los elementos
        element_names = [blob.name for blob in blobs]

        return element_names


bucket_service = BucketService()
