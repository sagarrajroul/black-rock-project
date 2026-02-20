FROM python:3.11-slim

WORKDIR /app

# prevent python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# expose the port and run the application
EXPOSE 5477
CMD ["uvicorn", "app:main.app","--host","0.0.0.0","--port","5477"]