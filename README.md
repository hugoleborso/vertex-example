# Image and Text Search Application

This repository contains the source code for an application that allows users to search for images using images or text.

## Features

- Text search
- Image search
- Image preview

## Technologies Used

- React
- TypeScript
- Tailwind CSS
- FastAPI
- Python
- Qdrant
- GCP Vertex AI Embeddings API

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3
- Docker
- A Vertex AI account

#### How to get a Gcp Vertex AI account
To get a GCP Vertex AI account, follow the instructions on the [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs/start/quickstart).

### Connect to your gcloud account in console
Follow the steps on the [gcloud doc](https://cloud.google.com/sdk/docs/install#mac)


### Setup

1. Clone the repository:

```bash
git clone https://github.com/hugoleborso/vertex-example.git
```

2. Install the dependencies

#### For the frontend
```bash
cd frontend
npm install
```

#### For the backend
```bash
cd backend
pip install -r requirements.txt
```

4. Set up the Qdrant database :
You can set up Qdrant using Docker. Run the following command to start the Qdrant service:
```bash
docker-compose up
```

5. Set up the Vertex AI account:
Follow the instructions on the Vertex AI documentation to create a new account and get your API key. Then, update the VERTEX_API_KEY in your environment variables with your new API key.

6. Start the application:
#### Start the frontend
```bash
cd frontend
npm start
```

#### Start the backend
```bash
cd backend
python main.py
```


### Adding images to the search engine
To add images to the search engine, you can use the following script:
```bash
python backend/load_image_embeddings.py <your image folder>
```

This allows images with extensions .jpg, .jpeg, .png to be added to the search engine.