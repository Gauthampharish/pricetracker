FROM python:3.12

# Set the working directory in the container
WORKDIR /PRICE_TRACKER

# Copy the project files to the working directory
COPY . .

# Install pip, setuptools, and wheel
RUN apt-get update && apt-get install -y python3-setuptools

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt
RUN pip install celery

# Run migrations
RUN python manage.py makemigrations identitymanagementserv alertsmanagementserv
RUN python manage.py migrate

# Expose the port that the Django server will run on
EXPOSE 8000

# Start the required services
CMD ["sh", "-c", "celery -A core worker --loglevel=info & python manage.py runserver 0.0.0.0:8000 & python manage.py run_websocket_client"]