FROM python:3.9.6-alpine3.14

WORKDIR /etl

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . /etl

CMD ["python",  "./main.py"]