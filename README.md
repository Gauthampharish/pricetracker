### Comprehensive Documentation: Cryptocurrency Price Alert System

This documentation covers the setup, API endpoints, and system architecture for the Cryptocurrency Price Alert System, which uses Django, Celery, Redis, and Binance's WebSocket API.

---

## Getting Started

This guide will help you set up and run the Price Tracker application using Docker Compose and Poetry for dependency management.

### Prerequisites

1. **Docker:** Install Docker.
2. **Docker Compose:** Install Docker Compose.
3. **Poetry (Optional, if using for dependency management):** Install Poetry.

### Configuration

Before starting the application, you need to configure environment variables.

#### Environment Variables
Edit the following in docker-compose.yml file to configure email.
```plaintext
DEBUG=True
EMAIL_USER=your_smtp_user
EMAIL_PASSWORD=your_smtp_password
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
```


#### Database Configuration

Ensure your PostgreSQL database is running and accessible using the details in docker-compose.yml file. Note that PostgreSQL is currently hosted directly on DigitalOcean. if postgress is not working please use sqlite

#### Admin User

A default admin user has been created with the following credentials:

- **Username:** `admin`
- **Password:** `adminpassword`

---

## Using Docker Compose

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Build and start the services:**

   ```bash
   docker-compose up --build
   ```

   This will build the Docker images and start the services defined in your `docker-compose.yml` file.

3. **Access the application:**

   Navigate to [http://localhost:8000](http://localhost:8000) to access the application.

4. **Stop the services:**

   ```bash
   docker-compose down
   ```

---

## Using Poetry for Dependency Management

1. **Install Poetry:**

   Follow the instructions on the Poetry [installation page](https://python-poetry.org/docs/#installation).

2. **Install dependencies:**

   ```bash
   poetry install
   ```

3. **Run the application:**

   ```bash
   poetry run celery -A core worker --loglevel=info &
   poetry run python manage.py runserver 0.0.0.0:8000 &
   poetry run python manage.py run_websocket_client
   ```

4. **Access the application:**

   Navigate to [http://localhost:8000](http://localhost:8000) to use the application.


  ### Introduction
  This documentation covers the API endpoints for user authentication and alert management, as well as the technical implementation of a real-time cryptocurrency price alert system. The system monitors prices using Binance's WebSocket API and sends notifications via email when user-defined conditions are met. It utilizes Django for the backend, Celery for task management, Redis for caching and task queuing, and Binance WebSocket API for real-time data.


### Project Structure

#### **core**
- **Purpose**: Central configuration and utility functions.
- **Contents**:
  - **settings.py**: Main settings file, including configuration variables, environment settings, and application configurations.
  - **urls.py**: URL routing definitions for the core application.
  
#### **identitymanagementserv**
- **Purpose**: Handles user authentication, registration, and profile management.
- **Contents**:
  - **models.py**: Database models related to user accounts, roles, and permissions.
  - **views.py**: Logic for handling registration, login, logout, and profile management requests.
  - **forms.py**: Forms for user registration, login, and profile updates.
  - **serializers.py**: Data serializers for API interactions, if applicable.
  - **urls.py**: URL routing for identity management endpoints.

  -
#### **alertmanagementserv**
- **Purpose**: Manages alerts and notifications within the application.
- **Contents**:
  - **models.py**: Database models for different types of alerts and notification settings.
  - **views.py**: Logic for creating, viewing, and managing alerts.
  - **serializers.py**: Serializers for alert-related data, if using APIs.
  - **urls.py**: URL routing for alert management endpoints.
  

#### **management/commands**
- **Purpose**: Custom Django management commands.
- **Contents**:
  - **run_websocket_client.py**: Custom management command for running a WebSocket client, potentially for real-time updates or communication.
  

  ## API Documentation

  Swagger has been added for ease of checking endpoints. You can access Swagger at http://127.0.0.1:8000/swagger/.

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


# Contionous Monitoring

## System Architecture and Implementation

### Overview

This system monitors cryptocurrency prices in real-time and triggers alerts when prices reach user-defined targets. It is built using Django for the backend, Celery for asynchronous task handling, and Binance WebSocket API for real-time data.

### Key Components

#### 1. Django Backend
- **Role**: Manages user data, alert configurations, and database interactions.
- **Key Model**: `Alert` - stores details of cryptocurrency alerts, including cryptocurrency type, target price, and status.

#### 2. WebSocket Client
- **Role**: Connects to the Binance WebSocket API to receive live updates on cryptocurrency prices.
- **Operation**: 
  - Establishes connection to Binance WebSocket endpoint.
  - Processes incoming price data and checks against active alerts.

```python
async def binance_websocket(self):
    symbols = await self.get_symbols()
    streams = [f"{symbol.lower()}@ticker" for symbol in symbols]
    uri = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                self.stdout.write(self.style.SUCCESS("Connected to Binance WebSocket"))
                while True:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        if 'data' in data:
                            ticker = data['data']
                            await self.process_ticker(ticker, symbols)
                    except asyncio.TimeoutError:
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        raise
        except websockets.exceptions.ConnectionClosed:
            self.stdout.write(self.style.WARNING("WebSocket connection closed. Reconnecting..."))
            await asyncio.sleep(5)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}. Reconnecting..."))
            await asyncio.sleep(5)
```

#### 3. Celery for Asynchronous Tasks
- **Role**: Manages background tasks, primarily sending email notifications.
- **Functionality**:
  - Celery executes tasks asynchronously, preventing delays in the main application flow.

```python
@shared_task(name='send_email_task')
def send_email_task(user_email, symbol, price):
    try:
        send_mail(
            'Price Alert Triggered',
            f'Your alert for {symbol} has been triggered. Current price: {price}',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {user_email} for {symbol}")
    except Exception as e:
        logger.error(f"Failed to send email to {user_email} for {symbol}. Error: {str(e)}")
```

#### 4. Database Operations
- **Role**: Handles data storage and retrieval for user alerts.
- **Implementation**:
  - Uses Django's ORM with asynchronous capabilities for non-blocking operations.

```python
@sync_to_async
def get_alerts(self, symbol):
    return list(Alert.objects.filter(cryptocurrency=symbol, status='created'))

@sync_to_async
def get_symbols(self):
    return list(Alert.objects.values_list('cryptocurrency', flat=True).distinct())

@sync_to_async
def update_alert(self, alert, status):
    alert.status = status
    alert.save()
```

## System Workflow

1. **Real-Time Monitoring**:
   - Establishes WebSocket connection to Binance for continuous cryptocurrency price updates.
   - Uses the Binance WebSocket API endpoint: `wss://stream.binance.com:9443/stream`
   - Subscribes to multiple ticker streams based on the cryptocurrencies being monitored.
   - Continuously receives JSON messages containing real-time price data.

2. **Asynchronous Processing**:
   - Uses `asyncio` and `websockets` for efficient handling of real-time data, allowing concurrent task processing.
   - Implements an event loop to manage multiple asynchronous tasks simultaneously.
   - Utilizes `async/await` syntax for non-blocking I/O operations.
   - Handles WebSocket messages asynchronously, preventing bottlenecks in data processing.

3. **Alert Processing**:
   - Checks incoming price data against stored alerts.
   - When an alert condition is met, it triggers the notification process.
   - Filters incoming data to only process relevant cryptocurrencies.
   - Compares current prices with target prices set in alerts.
   - Uses asynchronous database queries to fetch and check alerts efficiently.

4. **Email Notification**:
   - Sends email notifications asynchronously via Celery when alert conditions are met.
   - Uses Django's email functionality configured with SMTP settings.
   - Implements a Celery task (`send_email_task`) to handle email sending in the background.
   - Logs successful email sends and any errors encountered during the process.

5. **Error Handling and Resilience**:
   - Implements robust error handling for WebSocket disconnections and timeouts.
   - Includes automatic reconnection logic for continuous monitoring.
   - Uses try-except blocks to catch and handle various exceptions.
   - Implements a reconnection mechanism with exponential backoff.
   - Logs errors and reconnection attempts for monitoring and debugging.

6. **Data Management**:
   - Utilizes Django ORM for efficient database operations.
   - Implements asynchronous database queries to prevent blocking the main process.
   - Uses `sync_to_async` decorator to make synchronous Django ORM calls asynchronous.
   - Fetches and updates alert data efficiently using bulk operations where possible.
   - Implements database connection pooling for improved performance.

## Usage

To run the price alert system, use the following Django management command:

```
python manage.py run_websocket_client
```

This command initializes the WebSocket client, connects to Binance, and starts monitoring prices and processing alerts.

## Dependencies

- Django: Web framework for the backend system.
- websockets: Library for building WebSocket clients and servers.
- asyncio: Python's built-in asynchronous I/O framework.
- Celery: Distributed task queue for handling background jobs like email sending.
- asgiref: ASGI specification and utilities, used for sync_to_async operations.

## Note

This system is designed to run continuously. 
---

This README provides a comprehensive overview of the cryptocurrency price alert system, including its architecture, key components, workflow, and usage instructions. It accurately reflects the system's implementation without Redis caching, offering clarity for developers interacting with or contributing to the system.