FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir poetry==2.1.4
RUN poetry self add poetry-plugin-export
RUN poetry export --without-hashes --format=requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python3", "-u", "main.py"]
