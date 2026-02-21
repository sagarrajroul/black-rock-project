# FastAPI App Run Process

## 🛠 Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- Docker

---

## 📁 Project Structure
```text
fastapi-app/
│
├── app/
│ ├── main.py
│ ├── routers/
│ ├── models/
│ ├── utils/
│ ├── api/
│ │ ├── returns.py
│ │ └── performance.py
│ │ └── transactions.py
│
├── app/
│ ├── test_performance.py
│ ├── test_transactions.py
│ ├── test_returns.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```
## 🚀 How to Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5477
```

## 🚀 How to access Locally
```bash
http://localhost:5477
```
## 🚀 Access swagger
```bash
http://localhost:5477/docs
```
## 🚀 How to run TestCases Locally
```tesxt
make sure to be in the main folder before run
```
```bash
pytest
```

## 🐳 Run Docker Locally
### Build docker
```bash
docker build -t blk-hacking-ind-sagarraj-roul .
```

## Run docker container
```bash
docker run -d -p 5477:5477 blk-hacking-ind-sagarraj-roul
```
## Access application locally
```bash
http://localhost:5477
http://localhost:5477/docs
```

## 🐳 Run Docker directly
```bash
docker pull jarvisagar/blk-hacking-ind-sagarraj-roul
docker run -d -p 5477:5477 jarvisagar/blk-hacking-ind-sagarraj-roul
```

