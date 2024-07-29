  ## Comprehensive Documentation: Cryptocurrency Price Alert System

  To provide comprehensive instructions, you should include details on setting up environment variables and configuring the application. Here’s how you can add these instructions to your README file:

---

## Getting Started

This guide will help you set up and run the Price Tracker application using Docker Compose and Poetry for dependency management.

### Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Poetry** (Optional, if using for dependency management): [Install Poetry](https://python-poetry.org/docs/#installation)

### Configuration

Before starting the application, you need to configure some environment variables.

1. **Environment Variables:**

   Create a `.env` file in the root of your project directory and add the following environment variables:

   ```plaintext
   DEBUG=True
   EMAIL_USER=your_smtp_user
   EMAIL_PASSWORD=your_smtp_password
   EMAIL_HOST=smtp.your-email-provider.com
   EMAIL_PORT=587
   # Celery settings
  CELERY_BROKER_URL=redis://redis1:6379/1
  CELERY_RESULT_BACKEND=redis://redis1:6379/1
  CELERY_ACCEPT_CONTENT=json
  CELERY_TASK_SERIALIZER=json
  CELERY_RESULT_SERIALIZER=json
  CELERY_TIMEZONE=UTC

# Redis Cache settings
REDIS_LOCATION=redis://redis0:6379/0  
   ```

   - Replace the placeholder values with your actual configuration details.

2. **Database Configuration:**

   - Ensure your PostgreSQL database is running and accessible using the details provided in the `.env` file.
   - note postrgress is currently hosted directly in digital ocean

### Using Docker Compose

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Build and start the services:**

   ```bash
   docker-compose up --build
   ```

   - This will build the Docker images and start the services defined in your `docker-compose.yml` file.

3. **Access the application:**

   Navigate to `http://localhost:8000` to access the application.

4. **Stop the services:**

   ```bash
   docker-compose down
   ```

### Using Poetry for Dependency Management

1. **Install Poetry:**

   Follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).

2. **Install dependencies:**

   ```bash
   poetry install
   ```

3. **Run the application:**

   ```bash
   poetry run celery -A core worker --loglevel=info & poetry run python manage.py runserver 0.0.0.0:8000 & poetry run python manage.py run_websocket_client
   ```

4. **Access the application:**

   Navigate to `http://localhost:8000` to use the application.

---




  ### Introduction
  This documentation covers the API endpoints for user authentication and alert management, as well as the technical implementation of a real-time cryptocurrency price alert system. The system monitors prices using Binance's WebSocket API and sends notifications via email when user-defined conditions are met. It utilizes Django for the backend, Celery for task management, Redis for caching and task queuing, and Binance WebSocket API for real-time data.

  ## API Documentation

  ### Authentication

  #### Register
  - **Endpoint**: `POST /auth/register/`
  - **Description**: Registers a new user.
  - **Request Body**:
    ```json
    {
        "username": "string",
        "password": "string",
        "email": "string"
    }
    ```
  - **Responses**:
    - **Success (201 Created)**:
      ```json
      {
          "username": "string",
          "email": "string"
      }
      ```
    - **Error (400 Bad Request)**:
      ```json
      {
          "error": "string"
      }
      ```

  #### Login
  - **Endpoint**: `POST /auth/login/`
  - **Description**: Authenticates a user and returns a JWT token.
  - **Request Body**:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```
  - **Responses**:
    - **Success (200 OK)**:
      ```json
      {
        "refresh": "string",
        "access": "string"
      }
      ```
    - **Error (401 Unauthorized)**:
      ```json
      {
          "error": "string"
      }
      ```

  ### Alerts

  #### Create Alert
  - **Endpoint**: `POST /alerts/create/`
  - **Description**: Creates a new price alert for a specific cryptocurrency.
  - **Request Body**:
    ```json
    {
        "cryptocurrency": "string",
        "target_price": "number",
        "status": "string" 
    }
    ```
  - **Responses**:
    - **Success (201 Created)**:
      ```json
      {
          "id": "integer",
          "cryptocurrency": "string",
          "target_price": "number",
          "status": "string",
          "user": "integer"
      }
      ```
    - **Error (400 Bad Request)**:
      ```json
      {
          "error": "string"
      }
      ```

  #### Delete Alert
  - **Endpoint**: `DELETE /alerts/delete/{id}/`
  - **Description**: Deletes a specified alert.
  - **Path Parameter**:
    - `id`: The ID of the alert to delete.
  - **Responses**:
    - **Success (204 No Content)**
    - **Error (404 Not Found)**:
      ```json
      {
          "error": "string"
      }
      ```

  #### Fetch Alerts
  - **Endpoint**: `GET /alerts/`
  - **Description**: Retrieves all alerts created by the authenticated user.
  - **Responses**:
    - **Success (200 OK)**:
      ```json
      {
          "results": [
              {
                  "id": "integer",
                  "cryptocurrency": "string",
                  "target_price": "number",
                  "status": "string",
                  "user": "integer"
              },
              
          ],
          "count": "integer",
          "next": "url or null",
          "previous": "url or null"
      }
      ```
    - **Error (401 Unauthorized)**:
      ```json
      {
          "error": "string"
      }
      ```

  #### Example Response for Fetch Alerts
  ```json
  [
      {
          "id": 1,
          "cryptocurrency": "ADXETH",
          "target_price": 0.0,
          "status": "triggered"
      }
  ]
  ```

  ### Filtering and Pagination

  - **Pagination**: Use query parameters `page` and `page_size` to control the pagination of results.
    - **Example**: `GET /alerts/?page=2&page_size=10`

  - **Filtering**: Filter alerts by `status` or `cryptocurrency`.
    - **Example**: `GET /alerts/?status=active&cryptocurrency=bitcoin`

  ---

  ## System Architecture and Implementation

  ### Overview
  The system monitors cryptocurrency prices in real-time and triggers alerts when prices reach user-defined targets. It is built using Django for the backend, Celery for asynchronous task handling, Redis as a message broker and caching layer, and Binance WebSocket API for real-time data.

  ### Key Components

  #### 1. **Django Backend**
  - **Role**: Manages user data, alert configurations, and database interactions.
  - **Key Model**: `Alert` - stores details of the cryptocurrency alerts, including the cryptocurrency type, target price, and status.

  #### 2. **WebSocket Client**
  - **Role**: Connects to the Binance WebSocket API to receive live updates on cryptocurrency prices.
  - **Operation**:
    - Connects to the Binance WebSocket endpoint.
    - Processes incoming price data and checks against active alerts.

  **Code Snippet**:
  ```python
  import asyncio
  import websockets
  import json

  async def binance_websocket(self):
      uri = "wss://stream.binance.com:9443/ws/!ticker@arr"
      symbols = await self.get_symbols()
      async with websockets.connect(uri) as websocket:
          while True:
              response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
              data = json.loads(response)
              filtered_data = [ticker for ticker in data if ticker['s'] in symbols]
              for ticker in filtered_data:
                  await self.process_ticker(ticker, symbols)
  ```

  #### 3. **Celery and Redis**
  - **Role**: Manages background tasks, primarily sending email notifications.
  - **Functionality**:
    - Celery executes tasks asynchronously, preventing delays in the main application flow.
    - Redis queues these tasks, facilitating communication between Django and Celery.
    - Redis is also used for caching during data fetch operations to enhance performance and reduce database load.

  **Task Example**:
  ```python
  from celery import shared_task
  from django.core.mail import send_mail
  from django.conf import settings

  @shared_task
  def send_email_task(user_email, symbol):
      send_mail(
          'Price Alert Triggered',
          f'The target price for {symbol} has been reached.',
          settings.EMAIL_HOST_USER,
          [user_email],
          fail_silently=False,
      )
  ```

  #### 4. **Database and Caching Operations**
  - **Role**: Handles data storage and retrieval for user alerts, with Redis providing caching to improve efficiency.
  - **Implementation**:
    - Utilizes Django's ORM with asynchronous capabilities to ensure non-blocking operations.
    - Redis cache is used to store frequently accessed data, reducing database queries and improving response times.

  **Key Methods**:
  - `get_alerts`: Retrieves active alerts for a specific cryptocurrency, using caching to optimize performance.
  - `get_symbols`: Fetches unique cryptocurrency symbols from the database, with results cached in Redis.
  - `update_alert`: Updates the status of an alert when it is triggered.

  **Code Snippet**:
  ```python
  from asgiref.sync import sync_to_async
  from alertsmanagementserv.models import Alert
  from django.core.cache import cache

  @sync_to_async
  def get_alerts(self, symbol):
      cache_key = f"alerts_{symbol}"
      alerts = cache.get(cache_key)
      if not alerts:
          alerts = list(Alert.objects.filter(cryptocurrency=symbol, status='created'))
          cache.set(cache_key, alerts, timeout=60)  # Cache for 60 seconds
      return alerts

  @sync_to_async
  def get_symbols(self):
      cache_key = "unique_symbols"
      symbols = cache.get(cache_key)
      if not symbols:
          symbols = list(Alert.objects.values_list('cryptocurrency', flat=True).distinct())
          cache.set(cache_key, symbols, timeout=60)  # Cache for 60 seconds
      return symbols

  @sync_to_async
  def update_alert(self, alert, status):
      alert.status = status
      alert.save()
      cache.delete(f"alerts_{alert.cryptocurrency}")
  ```

  ### System Workflow

  1. **Real-Time Monitoring**:
    - The system establishes a WebSocket connection to Binance, receiving continuous updates on cryptocurrency prices.

  2. **Asynchronous Processing**:
    - The use of `asyncio` and `websockets` allows the system to handle real-time data efficiently, processing multiple tasks concurrently.

  3. **Email Notification**:
    - When an alert condition is met, an email notification is sent to the user. This process is handled asynchronously via Celery, ensuring it does not block other operations.

  4. **Error Handling and Resilience**:
    - The system includes robust error handling for WebSocket disconnections and timeouts, ensuring continuous monitoring and stability.

  5. **Caching with Redis**:
    - Redis is used for caching to improve data retrieval speeds and reduce the load on the database. Alerts and symbols are cached, and the cache is invalidated when relevant data changes.

  ---

  This documentation provides a comprehensive overview of both the API endpoints and the underlying architecture of the cryptocurrency price alert system, offering clarity and guidance for developers interacting with or contributing to the system.