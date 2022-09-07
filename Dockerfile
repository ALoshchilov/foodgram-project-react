FROM python:3.7-slim
WORKDIR /app
COPY ./backend/requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./backend/backend_project/ .
CMD ["gunicorn", "backend_project.wsgi:application", "--bind", "0:8000" ]