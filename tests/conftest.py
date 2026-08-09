"""
Test configuration and shared fixtures.

Uses a dedicated PostgreSQL test database so the production database is never touched.

Run locally:
    pytest -v

In CI the TEST_DATABASE_URL env var is set in the workflow file.
"""

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Test database URL — separate from production.
# Default matches the local dev Postgres (same host/user/pass, different DB).
# Override via TEST_DATABASE_URL env var in CI or other environments.
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:root@localhost:5432/test_tracker",
)

# ---------------------------------------------------------------------------
# Patch env vars BEFORE any app module is imported so that:
# 1. config.py validation sees a valid SECRET_KEY (min 32 chars)
# 2. settings.DATABASE_URL points at the test DB for the whole session
# ---------------------------------------------------------------------------
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-32x")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:5173")
os.environ.setdefault("UPLOAD_DIR", "uploads/resumes")

# ---------------------------------------------------------------------------
# Import app components AFTER env vars are set
# ---------------------------------------------------------------------------
from app.main import app                    # noqa: E402
from app.database import Base, get_db      # noqa: E402
from app.routers.auth import limiter as auth_limiter  # noqa: E402

# ---------------------------------------------------------------------------
# Build a test engine / session bound to the test database
# ---------------------------------------------------------------------------
test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override: serves test DB sessions to FastAPI route handlers."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Session-scoped fixture: create tables once, drop them after the whole run
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all ORM tables at session start; drop them when done."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ---------------------------------------------------------------------------
# Function-scoped fixture: wipe all rows between tests for full isolation
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def clean_tables():
    """Truncate every table after each test so no state bleeds across tests."""
    yield
    with test_engine.connect() as conn:
        conn.execute(
            text("TRUNCATE TABLE interviews, applications, users RESTART IDENTITY CASCADE")
        )
        conn.commit()


# ---------------------------------------------------------------------------
# TestClient fixture
#
# slowapi captures its key_func in a closure at decoration time, so patching
# _key_func after import has no effect. The correct approach is to call
# auth_limiter.reset() before each test — this clears the in-memory counters
# so each test starts with a fresh rate-limit budget.
# No production code is modified.
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    """TestClient with test-DB override; rate-limit storage reset each test."""
    app.dependency_overrides[get_db] = override_get_db

    # Clear slowapi's in-memory rate-limit counters before each test.
    # The router-level limiter (auth_limiter) uses in-memory storage by
    # default and supports reset(). Without this, limits from prior tests
    # accumulate because TestClient always presents the same fake IP.
    auth_limiter.reset()

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper: register a user and log in, returning ready-to-use auth headers
# ---------------------------------------------------------------------------
def create_user_and_login(
    client: TestClient,
    email: str,
    password: str = "securepassword123",
    name: str = "Test User",
) -> dict:
    """Register + login; return {"Authorization": "Bearer <token>"}."""
    client.post(
        "/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(client):
    """JWT auth headers for User A (the primary test user)."""
    return create_user_and_login(client, "usera@example.com")


@pytest.fixture
def auth_headers_b(client):
    """JWT auth headers for User B (the second test user for ownership tests)."""
    return create_user_and_login(client, "userb@example.com", name="User B")


# ---------------------------------------------------------------------------
# Canonical application payload — satisfies all schema validators:
#   company: min 2 chars, role: min 3 chars, salary: > 10000
# ---------------------------------------------------------------------------
SAMPLE_APPLICATION = {
    "company": "Acme Corp",
    "role": "Software Engineer",
    "salary": 120000,
    "status": "Applied",
}
