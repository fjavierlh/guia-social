FROM python:3.7.9-alpine3.13

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]