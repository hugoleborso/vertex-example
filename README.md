# Image and Text Search Application

This repository contains the source code for an application that allows users to search for images using images or text.

## Getting Started

### How to get a Gcp Vertex AI account
Start by creating your GCP account [here](https://console.cloud.google.com/?hl=fr) if you do not have one.
You can get a free trial account with $300 in credits to use for 90 days here: [GCP Free Trial](https://cloud.google.com/free/docs/free-cloud-features?hl=fr#free-trial)


### Connect to your gcloud account in terminal
Install the gcloud sdk from the [gcloud doc](https://cloud.google.com/sdk/docs/install#mac)

You can now now follows the instructions on the [Vertex GCP documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-multimodal-embeddings?hl=fr) to create a new project and enable the Vertex AI API.


### Setup

#### Clone the repository:

```bash
git clone https://github.com/hugoleborso/vertex-example.git
```

#### Install the dependencies

##### For the frontend
```bash
cd frontend
npm install
```

##### For the backend
```bash
python3.11 -m venv vertex-ex-venv
source vertex-ex-venv/bin/activate
cd backend
pip install -r requirements.txt
```

#### Set up the Qdrant database :
You can set up Qdrant using Docker. Run the following command to start the Qdrant service:
```bash
docker-compose up
```

#### Set up the Vertex AI account:
Follow the instructions on the Vertex AI documentation to create a new account and a project.
You can then copy the content of `.env.example` to a new file called `.env` and fill in the following variables:
```bash
MY_GCP_PROJECT_ID = YOUR_GCP_PROJECT_ID
MY_GCP_REGION = YOUR_GCP_REGION
```

#### Start the application:
##### Start the frontend
```bash
cd frontend
npm start
```

##### Start the backend
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

## Prerequisites

- Node.js and npm
- Python 3
- Docker
- A Vertex AI account