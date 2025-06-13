FROM python:3.10.0-slim-buster

WORKDIR /app

COPY . /app
COPY IMBD.csv /app

RUN pip install --upgrade pip
RUN pip install flask pandas matplotlib seaborn

EXPOSE 3000

CMD [ "python", "Analisis Movie.py" ]