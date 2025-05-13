from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.services.auth_service import get_current_user
from main import app


def override_get_current_user():
    return {
        "sub": "test_uid",
        "email": "test@example.com",
    }


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_current_user] = override_get_current_user

    # patch onde a função É USADA, não definida!
    with patch(
        "app.services.supabase_service.check_and_increment_usage", return_value=None
    ):
        with TestClient(app) as c:
            yield c

    app.dependency_overrides.clear()
