import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()

def test_root_endpoint(client):
    """Test the root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<html" in response.text
    assert "Toxicity Analysis Tester" in response.text

def test_analyze_single_text(client, mock_analyzer):
    """Test analyzing a single text"""
    request_data = {
        "texts": ["Hello world!"],
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert "processing_time" in data
    assert "request_id" in data
    assert "timestamp" in data
    
    result = data["results"][0]
    assert all(key in result for key in [
        "toxicity", "severe_toxicity", "obscene",
        "threat", "insult", "identity_attack"
    ])

def test_analyze_multiple_texts(client, mock_analyzer):
    """Test analyzing multiple texts"""
    request_data = {
        "texts": ["Hello world!", "This is a test.", "Another message."],
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["results"]) == 3

def test_analyze_empty_request(client):
    """Test analyzing with empty request"""
    request_data = {
        "texts": [],
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 422  # Validation error

def test_analyze_invalid_batch_size(client):
    """Test analyzing with invalid batch size"""
    request_data = {
        "texts": ["Hello world!"],
        "batch_size": 0  # Invalid batch size
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 422

def test_analyze_large_batch(client, mock_analyzer):
    """Test analyzing with large number of texts"""
    texts = ["Hello world!"] * 1001  # More than max allowed
    request_data = {
        "texts": texts,
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 422

def test_metrics_endpoint(client):
    """Test the metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "toxicity_api" in response.text

def test_analyze_text_validation(client):
    """Test text validation in analyze endpoint"""
    # Test with non-string text
    request_data = {
        "texts": [123],  # Invalid type
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 422

def test_analyze_response_format(client, mock_analyzer):
    """Test the format of analyze response"""
    request_data = {
        "texts": ["Hello world!"],
        "batch_size": 32
    }
    
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    result = data["results"][0]
    
    # Check all scores are between 0 and 1
    for score in result.values():
        assert 0 <= score <= 1
        assert isinstance(score, float)

def test_cors_headers(client):
    """Test CORS headers are properly set"""
    response = client.options("/analyze", headers={
        "origin": "http://localhost",
        "access-control-request-method": "POST"
    })
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_request_id_uniqueness(client, mock_analyzer):
    """Test that request IDs are unique"""
    request_data = {
        "texts": ["Hello world!"],
        "batch_size": 32
    }
    
    response1 = client.post("/analyze", json=request_data)
    response2 = client.post("/analyze", json=request_data)
    
    assert response1.json()["request_id"] != response2.json()["request_id"]