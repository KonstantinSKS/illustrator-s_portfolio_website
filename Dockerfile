FROM python:3.9
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY . .
COPY .env .env 
RUN pip install -r requirements.txt --no-cache-dir
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "victoria_site:app"]
# CMD ["python", "run.py"]

# НЕ ЗАБЫТЬ УБРАТЬ КОПИРОВАНИЕ .ENV!!!
# УЗНАТЬ ЕСТЬ ЛИ НА СЕРВЕРЕ УЖЕ УСТАНОВЛЕННЫЙ GUNICORN и NGINX?? 

# Билдим образ
# docker build -t konstantinsks/illustrator_site .

# Запуск контейнера из образа
# docker run --name illustrator_site_container --rm -p 5000:5000 illustrator_site

# Билдим volume для БД
# docker volume create <название>    pg_data
# Запуск контейнера из образа c volume
# docker run --name illustrator_site_container -p 5000:5000 -v pg_data:/instance konstantinsks/illustrator_site

# Загрузка образа на DockerHub
# docker push konstantinsks/illustrator_site:latest
# Обновление образа на хабе после изменения и пересборки
# docker push <imagename>

# Создание внутренней локальной сети для связи контейнеров
# docker network create flask-network 
# Подключим к сети контейнеры бэкенда и базы данных
# docker network connect flask-network flaskdb

# Поднять сеть контейнеров
# docker compose up
