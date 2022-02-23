# pull official base image
FROM python:3.10

# set work directory
WORKDIR ../urlshortener

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apt-get update && apt-get add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# copy entrypoint.sh
#COPY ./entrypoint.sh /
#RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
#ENTRYPOINT [".entrypoint.sh"]
