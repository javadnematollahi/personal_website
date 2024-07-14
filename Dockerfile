FROM python:3.11

WORKDIR /myapp

COPY . /myapp

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]

