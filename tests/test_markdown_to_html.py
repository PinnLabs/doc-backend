import io

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_convert_html_missing_file():
    response = client.post("/api/v1/markdown/convert-to-html/")
    assert response.status_code == 401  # Unprocessable Entity (missing required file)
