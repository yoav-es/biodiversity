FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for building wheels and for nbconvert
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

# default command: execute the notebook and keep container alive briefly
CMD ["bash", "-lc", "python -m nbconvert --to notebook --execute biodiversity.ipynb --output biodiversity-executed.ipynb --ExecutePreprocessor.timeout=600"]

