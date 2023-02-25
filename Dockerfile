FROM python:3.8
COPY ./requirements.txt app/requirements.txt
COPY . /app
WORKDIR app
EXPOSE 8070
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

