# FROM frolvlad/alpine-python-machinelearning:latest


# FROM jfloff/alpine-python:latest

# RUN pip install --upgrade pip

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# EXPOSE 4000

# ENTRYPOINT  ["python"]

# CMD ["app.py"]




FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

# RUN \
#  apk add --no-cache postgresql-libs && \
#  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
#  python3 -m pip install -r requirements.txt --no-cache-dir && \
#  apk --purge del .build-deps

COPY . .

EXPOSE 4000

CMD ["python3", "app.py"]