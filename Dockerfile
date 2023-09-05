FROM python:3.10

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYCODE 1

CMD ["python3", "main.py"]