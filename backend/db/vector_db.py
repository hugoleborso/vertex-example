from qdrant_client import QdrantClient  # type: ignore
from qdrant_client.http.models import models, Distance, VectorParams, PointStruct, ScoredPoint  # type: ignore


COLLECTION_NAME = "search_engine_embeddings"
EMBEDDING_SIZE = 1408


class VectorDB:
    def __init__(self):
        self.client = QdrantClient("http://0.0.0.0", port=6333)
        self.create_collection_if_not_exists()

    def create_collection_if_not_exists(self):
        existing_collections = self.client.get_collections()

        if COLLECTION_NAME not in [
            col.name for col in existing_collections.collections
        ]:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_SIZE, distance=Distance.COSINE
                ),
            )
            print(f"Collection '{COLLECTION_NAME}' created.")
        else:
            print(f"Collection '{COLLECTION_NAME}' already exists.")

    def insert(self, id: int, vector: list[float], payload):
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(id=id, vector=vector, payload=payload),
            ],
        )

    def insert_many(self, points: list[PointStruct]):
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    def search(self, vector: list[float], limit=10) -> list[tuple[dict | None, float]]:
        search_results: list[ScoredPoint] = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
        )
        return [
            (search_result.payload, search_result.score)
            for search_result in search_results
        ]
