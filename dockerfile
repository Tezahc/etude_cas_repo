# syntax=docker/dockerfile:1

FROM	python:3.8-slim-buster
WORKDIR /app

COPY	requirements.txt requirements.txt
RUN     pip install -r requirements.txt

COPY . .
EXPOSE 5432

CMD ["python3", "-m", "flask", "run", "-p=5432", "--host=0.0.0.0" ]