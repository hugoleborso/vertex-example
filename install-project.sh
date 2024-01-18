cd frontend
npm install
npm start
cd ..
docker-compose up -d
python3.11 -m venv vertex-ex-venv
source ./vertex-ex-venv/bin/activate
pip install -r requirements.txt
cd backend
python main.py
