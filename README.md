# C+A+D - Technical Assignment
This project is a submission for the Backend Developer position at Carbon+Alt+Delete. It demonstrates the implementation of a RESTful API using **FastAPI**, **PostgreSQL**, and **SQLAlchemy** for managing measurement data.

The main objective of the assignment is to showcase solid backend engineering practices including:
- RESTful API design
- Data validation and persistence
- Error handling
- Integration testing
- Project structure and maintainability
---
## 📁 Project Structure
- app/
  - ```apis.py```: API route definitions
  - ```crud.py```: Database interaction logic (Create, Read, Update, Delete)
  - ```database.py```: Database connection and session handling
  - ```dependencies.py```: Reusable dependencies for routes
  - ```models.py```: SQLAlchemy ORM models
  - ```schemas.py```: Pydantic schemas for request/response validation
- test/
  - ```conftest.py```: Pytest Configuration
  - ```test_measurements.py```: Pytest APIs test
- ```.env```: Environment variables for local development
- ```docker-compose.yml```: Multi-container Docker setup (API + PostgreSQL)
- ```Dockerfile```: API Docker image definition
- ```main.py```: Entry point for FastAPI app
- ```requirements.txt```: Python dependencies
- ```pytest.ini```: asyncio_default_fixture_loop_scope variable
- ```README.md```: Project documentation
---
## 🧱 Code Overview
### main.py
This is the entry point of the FastAPI application.
- Initializes the FastAPI app instance.
- Automatically creates all database tables using SQLAlchemy’s Base.metadata.create_all.
- Registers all API routes via include_router.
- Exposes a simple health check endpoint at / to confirm the app is running.
- Supports development mode execution using uvicorn for local server startup.
```
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```
### apis.py
Defines the RESTful endpoints for managing measurement records.
- Uses FastAPI’s APIRouter for clean routing separation.
- Depends on a reusable API key check via verify_api_key (middleware-style security).
- Implements:
  - ```POST /measurements/``` – Create a new measurement
  - ```GET /measurements/``` – List all measurements (with optional source filter)
  - ```GET /measurements/{id}``` – Retrieve a specific measurement
  - ```PUT /measurements/{id}``` – Update a measurement
  - ```DELETE /measurements/{id}``` – Remove a measurement

Error handling is implemented with HTTPException to return 404 if a record is not found.
### crud.py
Contains the business logic for database operations using SQLAlchemy ORM.
- ```get_measurements``` – Returns paginated results with optional filtering by source.
- ```get_measurement``` – Returns a single record by ID.
- ```create_measurement``` – Adds a new measurement to the database.
- ```update_measurement``` – Updates an existing record with partial update logic.
- ```delete_measurement``` – Deletes a record by ID if it exists.
The functions keep the logic modular and reusable from the API layer.
### database.py
Handles all database configuration and session management.
- Loads the ```DATABASE_URL``` from the ```.env``` file using ```python-dotenv```.
- Creates the SQLAlchemy engine and session factory (```SessionLocal```).
- Defines ```Base``` using SQLAlchemy's declarative system.
- Provides a FastAPI dependency (```get_db```) that opens and closes DB sessions automatically for each request.

This ensures each route handler gets a clean and properly managed database session.
### dependencies.py
Implements simple API key-based authentication.
- Loads the API key from the ```.env``` file.
- Defines a reusable dependency (```verify_api_key```) that checks the ```x-api-key``` header on incoming requests.
- If the key is missing or invalid, the request is rejected with a ```401 Unauthorized``` error.

Used as a lightweight security layer for protecting your endpoints.
### models.py
Defines the database model for the ```Measurement``` entity using SQLAlchemy ORM.
- ```id```: Auto-incrementing primary key.
- ```co2_value```: Required float field for CO₂ value.
- ```unit```: Optional string (defaults to ```"ppm"```).
- ```source```: Optional string (defaults to ```"unknown"```).
- ```description```: Optional string for additional context.

This schema directly maps to the ```measurements``` table in PostgreSQL.
### schemas.py
Defines Pydantic models for request validation and response serialization.
- ```MeasurementBase```: Shared attributes across create, update, and read operations.
- ```MeasurementCreate```: Inherits from ```MeasurementBase```, used for POST requests.
- ```MeasurementUpdate```: Same as ```MeasurementBase```, allows partial updates.
- ```MeasurementOut```: Adds ```id``` to the response and enables ORM compatibility with ```orm_mode```.

Ensures clean data parsing, validation, and serialization between client and server.
### conftest.py
Sets up the testing environment for FastAPI with pytest.
- ```pytest_configure(config)```: Configures the asyncio default fixture loop scope to avoid warnings.
- SQLite In-Memory Database:
  - ```engine```: Creates an in-memory SQLite database for isolated tests.
  - ```TestingSessionLocal```: Manages database sessions for tests.
- Fixtures:
- ```setup_database```: Resets the database before and after each test.
- ```db```: Provides a fresh database session for each test.
- ```client```: Provides a test client with the injected database session.
- ```auth_headers```: Provides a mock authorization header.

```conftest.py``` configures a test environment with an in-memory database, handling database setup, test client creation, and authorization for isolated and reliable tests.
### test_measurements.py
Tests FastAPI measurement endpoints.
- ```test_root_endpoint```: Checks if the root endpoint returns status 200 and the correct message.
- ```test_create_measurement```: Verifies creation of a new measurement.
- ```test_get_all_measurements```: Ensures multiple measurements can be fetched.
- ```test_get_measurements_by_source```: Tests filtering measurements by source.
- ```test_get_single_measurement```: Verifies fetching a measurement by ID.
- ```test_update_measurement```: Confirms updating a measurement works.
- ```test_delete_measurement```: Ensures measurement deletion returns 204 and subsequent GET returns 404.
- ```test_not_found```: Verifies 404 errors for non-existing measurements.
- ```test_unauthorized_access```: Tests 401 error for requests without an API key.

Ensures correct functionality of measurement API endpoints for CRUD operations and authorization handling.
### .env
Stores environment-specific configuration values.
```
API_KEY = api-key
POSTGRES_USER = db-user
POSTGRES_PASSWORD = db-password
POSTGRES_DB = db-name
TEST_BUILD=True
DATABASE_URL = postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```
- ```API_KEY```: The API key used for authentication.
- ```POSTGRES_USER```: Username for the PostgreSQL database.
- ```POSTGRES_PASSWORD```: Password for the PostgreSQL database.
- ```POSTGRES_DB```: Name of the PostgreSQL database.
- ```TEST_BUILD```: If True, runs tests in the test folder using pytest. If False, runs the API in Docker.
- ```DATABASE_URL```: PostgreSQL connection URL using the provided credentials.
### docker-compose.yml
Defines a multi-container Docker setup:
- ```web```: Runs the FastAPI app.
- ```db```: Runs a PostgreSQL database with health checks.
- Uses volumes for data persistence and ```.env``` for configuration.
- Ensures that the web service waits for the database to be healthy before starting.
### Dockerfile
Builds the Docker image for the FastAPI app.
- Starts from a slim Python 3.11 base image.
- Installs dependencies from ```requirements.txt```.
- Copies the application code.
- Runs the app using ```uvicorn```.
### requirements.txt
Lists all required Python packages:
- ```fastapi```, ```uvicorn```: Web framework and ASGI server.
- ```sqlalchemy```: ORM for database operations.
- ```pydantic```: Data validation.
- ```psycopg2-binary```: PostgreSQL driver.
- ```python-dotenv```: For environment variable loading.
- ```pytest```: For writing integration tests.
- ```httpx```:
- ```pytest-asyncio```: 
## How to Run and Test the Application
### 1. Set up the Environment
Ensure you have the necessary environment variables set in your .env file.
### 2. Run the API in Docker
- Make sure TEST_BUILD=False in .env.
- Make sure Docker is installed and running on your machine.
- Build and run the Docker containers using the following command:
```
docker-compose up --build
```
- This will start the API and PostgreSQL database containers.
### 3. Run Tests
- Make sure TEST_BUILD=True in .env.
- Tests are located in the test folder and use pytest for testing.
- To run the tests, use the following command:
```
pytest
```
- This will run all the tests in the test folder and provide a summary of the results.

### 4. API Endpoints
All endpoints require authentication using the API key defined in your ```.env``` file.
- API Key: The API key must be passed in the x-api-key header for all requests.
#### Endpoints:
- GET /measurements/
  - Description: Retrieves all measurements.
- POST /measurements/
  - Description: Creates a new measurement.
- GET /measurements/{id}
  - Description: Retrieves a specific measurement by ID.
- PUT /measurements/{id}
  - Description: Updates a specific measurement by ID.
- DELETE /measurements/{id}
  - Description: Deletes a specific measurement by ID.
- Authentication
  - Each request to the API must include the API key in the x-api-key header.
  - The value of x-api-key must match the key defined in the ```.env``` file.
### 5. Testing Information
- Ensure that your ```.env``` file is configured correctly to run the tests.
- The tests cover the following functionalities:
  - Create, read, update, and delete measurements.
  - Handling of unauthorized access (missing API key).
  - Error handling for not found resources.
### 6. Docker Compose
- Ensure that your ```.env``` file is configured correctly to run the Docker.
- If running in Docker, ensure you have the ```docker-compose.yml``` file in your project directory.
- The docker-compose.yml file should define the services, such as the API and PostgreSQL database, and how they are connected.
