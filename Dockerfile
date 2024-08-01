FROM python:latest 
COPY . /usr/src/
WORKDIR /usr/src/bushtree
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate
EXPOSE 6000
CMD ["python", "manage.py", "runserver", "0.0.0.0:6000"]
