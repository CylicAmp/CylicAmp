# test_matrix_stationarity.py
import json
import pytest
import numpy as np
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import our production systems
from MWS_NON_STATIONARY_AUDITOR_v5 import (
    app,
    get_db,
    Base,
    NonStationaryAuditLog,
    StatisticalNonStationarityAuditor,
    API_TOKEN_SECRET
)

# ====================== 1. ISOLATED SESSION CONFIGURATORS ======================
@pytest.fixture(scope="function")
def test_engine_factory():
    """
    Function-scoped engine factory. Instantiates a completely fresh,
    isolated in-memory SQLite database instance for every individual test.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session_local_factory(test_engine_factory):
    """Generates an independent, isolated session maker bound to the active test engine."""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine_factory)

@pytest.fixture(scope="function")
def clean_db_session(session_local_factory):
    """Provides an isolated database session to query and assert records directly within tests."""
    db = session_local_factory()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_client(session_local_factory):
    """
    Overrides the FastAPI database dependency graph dynamically.
    Guarantees thread-safe, isolated database sessions for background tasks.
    """
    def _override_get_db():
        db = session_local_factory()
        try:
            yield db
        finally:
            db.close()

    # Inject the override connection block into the active app context
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client
    # Clean up the dependency map post-execution to prevent module leakage
    app.dependency_overrides.clear()

# ====================== 2. DATA PAYLOAD MOCK FIXTURES ======================
@pytest.fixture(scope="function")
def mock_auditor_payload():
    """Provides a controlled, unrounded matrix request schema dictionary."""
    return {
        "url": "mock://isolated_verification_stream",
        "matrix_data": [
            [2.3, 3.2, 2.5, 3.5],
            [5.5, 7.2, 7.3, 7.5],
            [1.1, 1.2, 1.3, 1.5]
        ],
        "bootstrap_iterations": 150,
        "apply_detrending": True
    }

@pytest.fixture(scope="function")
def mock_statistical_returns():
    """Returns predictable statistical values to freeze execution paths."""
    return (
        0.088137,  # Simulated observed variance
        0.013300,  # Simulated empirical p-value (< 0.05)
        {"null_mean": 0.021, "null_ci_2_5": 0.004, "null_ci_97_5": 0.033}
    )

# ====================== 3. COMPREHENSIVE ISOLATED UNIT TESTS ======================
def test_security_header_authentication_challenge(test_client, mock_auditor_payload):
    """Guarantees the endpoint blocks execution and responds with 'Not authenticated' if token is absent."""
    response = test_client.post("/api/v1/audit/matrix-stationarity", json=mock_auditor_payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

def test_detrending_filter_neutralizes_slopes():
    """Verifies that the linear detrending matrix filter eliminates systematic mean drifts."""
    x = np.arange(10)
    # Generate arrays with explicit linear drift trends
    matrix_with_trend = np.array([4.2 * x + 2.0, -3.1 * x + 7.5])

    auditor = StatisticalNonStationarityAuditor(apply_detrending=True)
    detrended_result = auditor._detrend_matrix(matrix_with_trend)

    # Residual matrix elements must collapse cleanly to absolute zero
    np.testing.assert_array_almost_equal(detrended_result, np.zeros_like(matrix_with_trend), decimal=5)

def test_async_pipeline_saves_correct_metrics_to_db(
    test_client, clean_db_session, mock_auditor_payload, mock_statistical_returns
):
    """
    End-to-End Verification: Asserts that endpoints execute, calculate confidence
    bounds, and successfully serialize records down to long-term database tables.
    """
    headers = {"X-Audit-Token": API_TOKEN_SECRET}

    # Intercept calculation methods to inject our static test parameters cleanly
    with patch.object(
        StatisticalNonStationarityAuditor,
        'calculate_bootstrap_p_value',
        return_value=mock_statistical_returns
    ):
        response = test_client.post(
            "/api/v1/audit/matrix-stationarity",
            json=mock_auditor_payload,
            headers=headers
        )

    assert response.status_code == 202

    # Query our function-isolated db session to verify asynchronous persistence logs
    persisted_log = clean_db_session.query(NonStationaryAuditLog).filter_by(
        source_url=mock_auditor_payload["url"]
    ).first()

    assert persisted_log is not None
    assert persisted_log.observed_variance == mock_statistical_returns
    assert persisted_log.empirical_p_value == mock_statistical_returns
    assert persisted_log.is_significant_tti_violation is True

    # Decode JSON text fields to verify metadata compliance
    decoded_json = json.loads(persisted_log.raw_json_payload)
    assert decoded_json["statistical_results"]["is_significant_tti_violation"] is True
    assert decoded_json["analysis_metadata"]["bootstrap_iterations"] == 150
