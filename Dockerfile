FROM python:3.9
WORKDIR /app
COPY . .
COPY .env .env
RUN pip install -r requirements.txt --no-cache-dir
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "run.py"]