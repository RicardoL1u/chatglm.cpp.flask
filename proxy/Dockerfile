FROM python:3.10-slim
WORKDIR /app
ADD . /app
RUN pip install requests
RUN pip install Flask

CMD ["python", "glm_server.py"]
