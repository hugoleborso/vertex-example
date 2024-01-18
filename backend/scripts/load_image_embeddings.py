import time
from tqdm import tqdm  # type: ignore
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

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


def load_image_embeddings(dataset_folder: str) -> tuple[list[list[float]], list[Path]]:
    """Computes embeddings for the images of the dataloader using Vertex AI endpoint."""
    all_images_path = []

    with ThreadPoolExecutor() as executor:
        futures = []

        extensions = ["*.jpg", "*.png", "*.jpeg"]
        all_image_paths = [
            path
            for ext in extensions
            for path in Path(dataset_folder).glob("**/" + ext)
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
