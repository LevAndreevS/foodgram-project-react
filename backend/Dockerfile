FROM python:3.9-slim
RUN mkdir /app
RUN pip install gunicorn==20.1.0
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app/foodgram
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]