import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils import ToxicityAnalyzer

@pytest.fixture
def client():
    """Create a test client fixture"""
    return TestClient(app)

@pytest.fixture
def mock_analyzer(mocker):
    """Mock the ToxicityAnalyzer to avoid actual model inference during tests"""
    mock_results = {
        'toxicity': [0.1],
        'severe_toxicity': [0.05],
        'obscene': [0.02],
        'threat': [0.01],
        'insult': [0.03],
        'identity_attack': [0.01]
    }
    
    mocker.patch.object(
        ToxicityAnalyzer, 
        'analyze_batch',
        return_value=[{
            'toxicity': 0.1,
            'severe_toxicity': 0.05,
            'obscene': 0.02,
            'threat': 0.01,
            'insult': 0.03,
            'identity_attack': 0.01
        }]
    )
    
    return mock_results

@pytest.fixture
def sample_texts():
    """Sample texts for testing"""
    return [
        "Hello world!",
        "This is a test.",
        "Another test message."
    ]

@pytest.fixture
def sample_request():
    """Sample request body"""
    return {
        "texts": ["Hello world!"],
        "batch_size": 32
    }