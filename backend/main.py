import os
import base64

import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from db import VectorDB
from vertex import EmbeddingsClient

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

os.makedirs("engine-imgs", exist_ok=True)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
