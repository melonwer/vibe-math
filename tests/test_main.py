"""Tests for Vibe Math API"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

class TestSolveEndpoints:
    """Test solve endpoints"""
    
    def test_solve_with_invalid_file_type(self):
        """Test solve endpoint with invalid file type"""
        response = client.post(
            "/solve",
            files={"file": ("test.txt", b"not an image", "text/plain")}
        )
        
        assert response.status_code == 400
    
    def test_solve_json_with_invalid_payload(self):
        """Test solve-json endpoint with invalid payload"""
        response = client.post(
            "/solve-json",
            json={"image": ""}
        )
        
        assert response.status_code == 422
    
    def test_solve_json_with_missing_field(self):
        """Test solve-json endpoint with missing image field"""
        response = client.post(
            "/solve-json",
            json={}
        )
        
        assert response.status_code == 422

class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_json_payload(self):
        """Test invalid JSON payload"""
        response = client.post(
            "/solve-json",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422