FROM python:3.13

COPY requirements.txt /docker/requirements.txt

WORKDIR /docker

RUN pip install --no-cache-dir -r requirements.txt

COPY . /docker/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]