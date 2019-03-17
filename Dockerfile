# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
# and copy the local contents into the container at /app
ADD ./src /app/src
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN mkdir -p /app/logs
RUN touch /app/logs/mylog.log

# Install dependencies
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV BOOKS_API_TOKEN AIzaSyCOeFB-k532HjyVfsYJK9pKKx9UGDoqq5g

# Run app.py when the container launches
CMD ["/usr/local/bin/gunicorn", "-b", ":80", "src.main.wsgi"]
