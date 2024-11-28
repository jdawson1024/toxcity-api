# Toxicity Analysis API

A high-performance API for text toxicity analysis using the Detoxify model. This API provides real-time toxicity analysis for text content with support for batch processing.

## Features

- High-performance text toxicity analysis
- Batch processing support
- Docker containerization
- Prometheus metrics
- Structured logging
- Request tracking and monitoring

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/toxicity-api.git
cd toxicity-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the API:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker Deployment

Build and run with docker-compose:
```bash
docker-compose up --build
```

## API Usage

Analyze texts for toxicity:
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": ["Hello world", "This is a test"],
       "batch_size": 32
     }'
```

Example response:
```json
{
  "results": [
    {
      "toxicity": 0.023,
      "severe_toxicity": 0.001,
      "obscene": 0.002,
      "threat": 0.001,
      "insult": 0.003,
      "identity_attack": 0.001
    }
  ],
  "processing_time": 0.543,
  "request_id": "abc123def",
  "timestamp": "2024-11-28T12:34:56.789Z"
}
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Key environment variables:
- `DEBUG`: Enable debug mode
- `BATCH_SIZE`: Default batch size for processing
- `MAX_WORKERS`: Number of worker threads
- `LOG_LEVEL`: Logging level (INFO/DEBUG/ERROR)
- `ALLOW_ORIGINS`: CORS allowed origins

## Error Handling

The API returns standard HTTP status codes:
- 200: Successful request
- 400: Invalid request
- 500: Server error

Each error response includes a detail message explaining the issue.

## Performance Considerations

- Use batch processing for multiple texts
- Keep batch sizes reasonable (recommended: 32-128)
- Monitor processing times in responses

## Security

To secure this API in production, consider:
- Adding authentication (API keys, JWT, etc.)
- Using HTTPS
- Implementing rate limiting
- Adding request validation

## Metrics

The API exposes Prometheus metrics at `/metrics` including:
- Request counts and latencies
- Text processing statistics
- System metrics

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request