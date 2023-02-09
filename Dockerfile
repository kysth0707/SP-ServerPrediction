FROM python:3.7.8

RUN pip install fastapi
RUN pip install uvicorn[standard]
RUN pip install keras
RUN pip install tensorflow

RUN mkdir -p /test
WORKDIR /test

ENTRYPOINT ["python", "server.py"]