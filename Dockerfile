FROM python:3.12
COPY . /usr/src/
WORKDIR /usr/src/solaris
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install setuptools
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
