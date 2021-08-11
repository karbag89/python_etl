FROM python:3.9.6-alpine3.14

WORKDIR /etl

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /etl

CMD ["python",  "./main.py"]