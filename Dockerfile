FROM python:3.10-slim

WORKDIR /python-chatroom
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY server.py ./
COPY main.py ./

EXPOSE 8000

CMD ["python", "main.py", "run-server"]