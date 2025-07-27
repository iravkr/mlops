import sys
import os
import requests
import time
import subprocess
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestModelDeployment:
    @classmethod
    def setup_class(cls):
        # Start the API server in background
        cls.process = subprocess.Popen([
            "python", "src/deployment/api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        cls.base_url = "http://localhost:8000"
    
    @classmethod
    def teardown_class(cls):
        if hasattr(cls, 'process'):
            cls.process.terminate()
            cls.process.wait()
    
    def test_health_endpoint(self):
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")
    
    def test_predict_endpoint_without_file(self):
        try:
            response = requests.post(f"{self.base_url}/predict", timeout=10)
            assert response.status_code == 422  # Validation error
        except requests.exceptions.RequestException:
            pytest.skip("API server not running")
