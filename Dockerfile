FROM python:3.11

# Set the working directory in the container
WORKDIR /PRICE_TRACKER

# Copy the requirements file to the working directory
COPY . .

# Install the project dependencies
RUN pip install poetry
RUN poetry install

# Run migrations
#RUN poetry run python manage.py makemigrations identitymanagementserv alertsmanagementserv
#RUN poetry run python manage.py migrate
# Expose the port that the Django server will run on
EXPOSE 8000

# Start the required services
CMD ["sh", "-c", " poetry run celery -A core worker --loglevel=info & poetry run python manage.py runserver 0.0.0.0:8000 & poetry run python manage.py run_websocket_client"]