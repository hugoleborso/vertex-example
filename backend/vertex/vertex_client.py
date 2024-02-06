import os
import base64
from google.cloud import aiplatform  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from dotenv import load_dotenv


load_dotenv(".env")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_REGION = os.getenv("GCP_REGION")

class EmbeddingsClient:
    def __init__(self) -> None:
        self.project_id = GCP_PROJECT_ID
        self.location = GCP_REGION
        self.endpoint = (
            f"projects/{self.project_id}/locations/{self.location}"
            "/publishers/google/models/multimodalembedding@001"
        )

        self.client_options = {
            "api_endpoint": f"{self.location}-aiplatform.googleapis.com"
        }
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options=self.client_options
        )

    def get_image_embeddings(self, image_bytes: bytes) -> list[float]:
        instance = struct_pb2.Struct()
        encoded_content = base64.b64encode(image_bytes).decode("utf-8")
        image_struct = instance.fields["image"].struct_value
        image_struct.fields["bytesBase64Encoded"].string_value = encoded_content

        request = aiplatform.gapic.PredictRequest()
        request.endpoint = self.endpoint
        request.instances.append(instance)
        predictions = self.client.predict(request).predictions
        if image_bytes:
            image_emb_value = predictions[0]["imageEmbedding"]
            return [v for v in image_emb_value]
        return []

    def get_text_embeddings(self, text: str) -> list[float]:
        print("Getting text embeddings for text:", text)
        instance = struct_pb2.Struct()
        text_struct = instance.fields["text"].struct_value
        text_struct.fields["content"].string_value = text

        request = aiplatform.gapic.PredictRequest()
        request.endpoint = self.endpoint
        request.instances.append(instance)
        predictions = self.client.predict(request).predictions
        if predictions:
            text_emb_value = predictions[0]["textEmbedding"]
            return [v for v in text_emb_value]
        return []

    def get_embedding(self, text: str | None = None, image_bytes: bytes | None = None):
        if not text and not image_bytes:
            raise ValueError("At least one of text or image_file must be specified.")

        instance = struct_pb2.Struct()
        if text:
            instance.fields["text"].string_value = text

        if image_bytes:
            encoded_content = base64.b64encode(image_bytes).decode("utf-8")
            image_struct = instance.fields["image"].struct_value
            image_struct.fields["bytesBase64Encoded"].string_value = encoded_content

        instances = [instance]

        response = self.client.predict(endpoint=self.endpoint, instances=instances)

        if text:
            text_emb_value = response.predictions[0]["textEmbedding"]
            text_embedding = [v for v in text_emb_value]
            return text_embedding

        elif image_bytes:
            image_emb_value = response.predictions[0]["imageEmbedding"]
            image_embedding = [v for v in image_emb_value]
            return image_embedding

        return []
