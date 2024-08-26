FROM python:3.9
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY . .
# COPY .env .env 
RUN pip install -r requirements.txt --no-cache-dir
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "victoria_site:app"]
# CMD ["python", "run.py"]
