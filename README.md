# Django Microservice with Background Processing

This repository contains a Django-based microservice that provides a REST API for background task processing using Celery and Redis. The entire application is containerized with Docker and deployed to AWS using Terraform and k3s.

## Architecture

The application consists of the following components:

- **Django Web Application**: Handles HTTP requests and provides REST API
- **Celery Worker**: Processes background tasks asynchronously
- **Redis**: Acts as message broker for Celery and result backend
- **PostgreSQL**: Database for storing task information
- **Docker**: Containerization of all components
- **Kubernetes (k3s)**: Orchestrates containers in production
- **AWS**: Cloud infrastructure provider
- **Terraform**: Infrastructure as Code tool for AWS provisioning
- **GitHub Actions**: CI/CD pipeline for testing, building, and deployment

## API Endpoints

- `POST /api/process/`: Queue a new task with email and message
- `GET /api/status/<task_id>/`: Check the status of a queued task
- `GET /swagger/`: API documentation using Swagger UI
- `GET /redoc/`: API documentation using ReDoc

## Local Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/William-eng/Django-microservice.git
   cd django-microservice
   ```

2. Create a .env file from the example:
   ```bash
   cp .env.example .env
   ```

3. Start the application with Docker Compose:
   ```bash
   docker compose up -d
   ```

4. Apply migrations:
   ```bash
   docker compose exec web python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. Access the application at http://localhost:8000

## Production Deployment

### Prerequisites

- AWS Account
- SSH key pair for EC2 access
- Terraform installed locally
- AWS CLI configured with appropriate permissions

### Deployment Steps

1. Initialize Terraform:
   ```bash
   cd terraform
   terraform init
   ```

2. Create `terraform.tfvars` file with your variables:
   ```hcl
   aws_region        = "us-east-1"
   key_name          = "your-key-pair-name"
   private_key_path  = "~/.ssh/your-key.pem"
   ```

3. Apply Terraform configuration:
   ```bash
   terraform apply
   ```

4. Setup GitHub repository secrets for CI/CD:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (generate this in Docker Hub account settings)
   - `EC2_PUBLIC_IP`: Public IP of the EC2 instance (from Terraform output)
   - `SSH_PRIVATE_KEY`: SSH private key content

5. Push code to the main branch to trigger the CI/CD pipeline:
   ```bash
   git push origin main
   ```

## Testing the API

Once deployed, you can test the API using curl:

```bash
# Queue a new task
curl -X POST http://your-load-balancer-url/api/process/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "message": "Hello World"}'

# Check task status
curl -X GET http://your-load-balancer-url/api/status/your-task-id/
```

## Infrastructure Details

The application is deployed on AWS with the following components:

- **VPC**: Isolated network for the application
- **EC2 Instance**: Hosts the k3s Kubernetes cluster
- **ECR**: Container registry for Docker images
- **k3s**: Lightweight Kubernetes for container orchestration

## CI/CD Pipeline

The GitHub Actions workflow performs:

1. **Testing**: Runs unit tests
2. **Building**: Builds the Docker image
3. **Pushing**: Pushes the image to AWS ECR
4. **Deploying**: Updates the Kubernetes deployment on k3s

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
