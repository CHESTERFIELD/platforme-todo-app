# pull official base image
FROM python:3.9.5-alpine

# set default python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy project
COPY ./src /usr/src/app/

# set work directory
WORKDIR /usr/src/app

EXPOSE 8000

# copy entrypoint.sh and grant with execute permission
# copied into "/usr/src" since "/usr/src/app" doesn't work for MacOS
COPY ./build/docker/web/entrypoint.sh /usr/src/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/entrypoint.sh \
    && chmod +x /usr/src/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
