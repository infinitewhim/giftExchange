# Dockerfile

FROM python:3.8-slim

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
# Set environment variables
ENV PYTHONUNBUFFERED 1         # Ensures output is logged directly
# Expose the port Django runs on
EXPOSE 8080

# Command to run the application
# For development purpose
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

# For production purpose
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "giftExchange.wsgi:application"]
