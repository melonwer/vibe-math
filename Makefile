.PHONY: help install dev-install test lint format run docker-build docker-run clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  dev-install  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  run          Run the application"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker"
	@echo "  clean        Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

dev-install:
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v --cov=app --cov-report=html

# Code quality
lint:
	flake8 app tests
	mypy app

format:
	black app tests
	isort app tests

# Development
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker
docker-build:
	docker build -t vibe-math .

docker-run:
	docker-compose up --build

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage