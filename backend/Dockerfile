FROM python:3.7-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY backend_project/ .
CMD ["gunicorn", "backend_project.wsgi:application", "--bind", "0:8000" ]