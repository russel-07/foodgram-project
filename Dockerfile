FROM python:3.8.5
WORKDIR /code    
COPY . ./        
RUN pip install -r /code/requirements.txt
WORKDIR /code/foodgram_project
CMD python manage.py collectstatic --no-input && \
    python manage.py migrate && \
    python manage.py loaddata fixtures.json && \
    gunicorn foodgram_project.wsgi:application --bind 0.0.0.0:8000
