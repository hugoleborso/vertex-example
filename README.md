# Image and Text Search Application

This repository contains the source code for an application that allows users to search for images and text.

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
- Vertex AI

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3
- Docker
- A Vertex AI account

#### How to get a Gcp Vertex AI account
To get a GCP Vertex AI account, follow the instructions on the [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs/start/quickstart).


### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
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
Set up the Qdrant database :
You can set up Qdrant using Docker. Run the following command to start the Qdrant service:
```bash
docker-compose up
```

4. Set up the Vertex AI account:
Follow the instructions on the Vertex AI documentation to create a new account and get your API key. Then, update the VERTEX_API_KEY in your environment variables with your new API key.

5. Start the application:
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