# Requirements Integration

All required packages for demo and integration are installed:
- fastapi
- uvicorn
- requests

API endpoints and frontend demo are integrated in run_local_server.py.

To run:
1. Start server: python run_local_server.py
2. Access demo endpoint: http://localhost:8000/hello
3. Access sample frontend: http://localhost:8000/sample_frontend

Tests can be run with: python test_hello_api.py
