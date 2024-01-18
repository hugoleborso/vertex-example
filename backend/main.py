import os
import base64
import shutil
from fastapi.staticfiles import StaticFiles
import uvicorn

from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

from db import VectorDB
from vertex import EmbeddingsClient
from scripts.load_image_embeddings import load_image_embeddings

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
vector_db = VectorDB()
embeddings_client = EmbeddingsClient()


ALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="engine-imgs"), name="images")


class TextQuery(BaseModel):
    text: str


class ImageQuery(BaseModel):
    image_bytes: str


@app.post("/search-text")
def search_text(query: TextQuery):
    print(f"Received text query: {query.text}")
    embeddings = embeddings_client.get_embedding(text=query.text)
    hits = vector_db.search(embeddings)
    res = []
    for hit, score in hits:
        if hit is not None:
            res.append(
                {
                    "imageUrl": f"images/{hit['image_path']}",
                    "imageName": hit["image_path"],
                    "percentage": score * 100,
                }
            )

    return res


@app.post("/search-image")
def search_image(query: ImageQuery):
    print(f"Received image query")
    image_bytes = base64.b64decode(query.image_bytes.split(",")[1])
    embeddings = embeddings_client.get_embedding(image_bytes=image_bytes)
    hits = vector_db.search(embeddings)
    res = []
    for hit, score in hits:
        if hit is not None:
            res.append(
                {
                    "imageUrl": f"images/{hit['image_path']}",
                    "imageName": hit["image_path"],
                    "percentage": score * 100,
                }
            )

    return res


@app.post("/store-images")
def store_images(dataset_folder: str):
    print(f"Computing embeddings for dataset in folder: {dataset_folder}")

    os.makedirs("engine-imgs", exist_ok=True)
    for file in Path(dataset_folder).rglob("*"):
        if file.suffix in ALLOWED_FILE_EXTENSIONS:
            shutil.copy2(file, "engine-imgs")

    embeddings, images_path = load_image_embeddings(dataset_folder)
    print(f"Inserting {len(embeddings)} embeddings into the database.")
    for i, embedding in enumerate(embeddings):
        vector_db.insert(i, embedding, {"image_path": str(images_path[i].name)})
    return {"message": "Embeddings computed and inserted into the database."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
