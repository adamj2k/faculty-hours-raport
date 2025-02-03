# Faculty Hours Report Service

A microservice for generating and managing faculty workload reports as part of the Faculty Hours system.

## Tech Stack

- **Programming Language**: Python
- **Framework**: FastAPI
- **Database**: MongoDB
- **Message Broker**: RabbitMQ
- **Dependencies**:
  - motor (MongoDB async driver)
  - pika (RabbitMQ client)
  - pandas (Data processing)
  - pydantic (Data validation)
  - uvicorn (ASGI server)

## Service Architecture

This service is part of a microservices architecture and is responsible for:
- Generating teacher workload reports
- Creating personal workload reports
- Producing summary department reports
- Storing reports in MongoDB
- Consuming messages from RabbitMQ queues

## Setup Instructions

1. **Environment Variables**
   Create a `.env` file with the following variables:
   ```
   MONGO_INITDB_ROOT_USERNAME=<username>
   MONGO_INITDB_ROOT_PASSWORD=<password>
   FH_APP_FACULTY_URL=<faculty_service_url>
   RABBITMQ_USER=<rabbitmq_username>
   RABBITMQ_PASSWORD=<rabbitmq_password>
   RABBITMQ_HOST=<rabbitmq_host>
   ```

2. **Docker Setup**
   ```bash
   # Build the Docker image
   docker build -t faculty-hours-report .

   # Run the container
   docker run -d \
     --name faculty-hours-report \
     -p 8200:8200 \
     --env-file .env \
     faculty-hours-report
   ```

   Using Docker Compose (recommended):
   ```bash
   # Start all services
   docker-compose up -d

   # View logs
   docker-compose logs -f faculty-hours-report

   # Stop all services
   docker-compose down
   ```

   The service will be available at `http://localhost:8200`

## Service Connections

The service interacts with several other components:

1. **MongoDB**
   - Stores three types of reports:
     - Teachers reports
     - Personal workload reports
     - Summary department reports

2. **RabbitMQ Message Queues**
   - Consumes messages from:
     - teacher-report-queue
     - personal-report-queue
     - summary-report-queue

3. **Faculty Service**
   - Fetches faculty data through HTTP endpoints
   - URL configured via `FH_APP_FACULTY_URL`

## API Documentation

Once the service is running, access the API documentation at:
- Swagger UI: `http://localhost:8200/docs`
- ReDoc: `http://localhost:8200/redoc`

## Development

The service uses FastAPI's async features and MongoDB's motor driver for non-blocking database operations. Report generation is triggered by messages received through RabbitMQ queues.
