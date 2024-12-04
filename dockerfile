# syntax=docker/dockerfile:1

FROM	python:3.11-bullseye
WORKDIR /app

COPY	requirements.txt requirements.txt
RUN     pip install -r requirements.txt

COPY    app/. .
EXPOSE  5000
# ENV     FLASK_APP=app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]