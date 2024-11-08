FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "web", "run", "--debug", "--host=0.0.0.0"]
