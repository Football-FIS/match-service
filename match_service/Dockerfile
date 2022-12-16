
# syntax=docker/dockerfile:1.4

FROM python:3.10-alpine AS builder
EXPOSE 8000
WORKDIR /match_service
COPY requirements.txt /match_service
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /match_service
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]