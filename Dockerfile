FROM python:3.11.6-slim-bullseye

WORKDIR /home/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "fastapi", "run", "main.py" ]