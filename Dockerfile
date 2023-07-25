FROM python:3.10-slim
WORKDIR /app
ADD . /app

RUN apt-get update && apt-get install -y \
    build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install Flask
RUN pip install -U chatglm-cpp

CMD ["python", "chatglm_server.py"]
