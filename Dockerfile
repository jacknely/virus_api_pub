FROM python:3.7-slim
WORKDIR /opt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]