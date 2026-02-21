# FastAPI App Run Process

## 🛠 Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- Docker

---

## 📁 Project Structure
fastapi-app/
│
├── app/
│ ├── main.py
│ ├── routers/
│ ├── models/
│ ├── utils/
│ ├── api/
│ │ ├── health.py
│ │ └── users.py
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md

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

