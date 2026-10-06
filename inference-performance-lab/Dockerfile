FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY configs ./configs
COPY datasets ./datasets
COPY dashboard.py ./
RUN mkdir -p /app/results
CMD ["uvicorn", "inference_lab.api:app", "--host", "0.0.0.0", "--port", "8006"]

