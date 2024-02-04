import argparse
import os
import shutil
import time
from tqdm import tqdm  # type: ignore
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from db import VectorDB  # type: ignore
from vertex import EmbeddingsClient  # type: ignore


def load_image_bytes(img_path):
    with open(img_path, "rb") as image_file:
        img_bytes = image_file.read()
        return img_bytes


def get_image_embeddings(img_bytes):
    embed_client = EmbeddingsClient()
    return embed_client.get_embedding(image_bytes=img_bytes)


requests_per_minute = 120
request_interval = (60 / requests_per_minute) * 1.10  # 10 % margin for safety
ALLOWED_FILE_EXTENSIONS = [".jpg", ".png", ".jpeg"]


def load_image_embeddings(dataset_folder: str) -> tuple[list[list[float]], list[Path]]:
    """Computes embeddings for the images of the dataloader using Vertex AI endpoint."""
    all_images_path = []

    with ThreadPoolExecutor() as executor:
        futures = []

        all_image_paths = [
            path
            for path in Path(dataset_folder).rglob("*")
            if path.suffix in ALLOWED_FILE_EXTENSIONS
        ]

        progress_bar = tqdm(
            total=len(all_image_paths), desc="Getting embeddings from dataset images"
        )

        for image_path in all_image_paths:
            all_images_path.append(image_path)
            image_bytes = load_image_bytes(image_path)

            # do not exceed the rate limit of the Vertex API
            time.sleep(request_interval)

            futures.append(executor.submit(get_image_embeddings, image_bytes))
            progress_bar.update()

        all_embeddings = [future.result() for future in futures]

        progress_bar.close()

    return (all_embeddings, all_images_path)


def main():
    parser = argparse.ArgumentParser(
        description="Compute embeddings for images using Vertex AI."
    )
    parser.add_argument(
        "dataset_folder", type=str, help="The folder containing the dataset images."
    )
    args = parser.parse_args()
    dataset_folder = args.dataset_folder
    vector_db = VectorDB()
    print(f"Computing embeddings for dataset in folder: {dataset_folder}")

    os.makedirs("backend/engine-imgs", exist_ok=True)
    for file in Path(dataset_folder).rglob("*"):
        if file.suffix in ALLOWED_FILE_EXTENSIONS:
            shutil.copy2(file, "backend/engine-imgs")

    embeddings, images_path = load_image_embeddings(dataset_folder)
    print(f"Inserting {len(embeddings)} embeddings into the database.")
    for i, embedding in enumerate(embeddings):
        vector_db.insert(i, embedding, {"image_path": str(images_path[i].name)})
    return {"message": "Embeddings computed and inserted into the database."}


if __name__ == "__main__":
    main()
