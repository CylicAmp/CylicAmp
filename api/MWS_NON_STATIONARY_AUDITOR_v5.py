"""
MWS_NON_STATIONARY_AUDITOR_v5.py

Statistical non-stationarity auditor with bootstrap p-value estimation,
linear detrending, and SQLAlchemy persistence via FastAPI.
"""

import json
from typing import List

import numpy as np
from scipy import signal
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATABASE_URL = "sqlite:///./mws_audit.db"
API_TOKEN_SECRET = "mws-audit-secret-token-2026"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NonStationaryAuditLog(Base):
    __tablename__ = "non_stationary_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, index=True)
    observed_variance = Column(Float)
    empirical_p_value = Column(Float)
    is_significant_tti_violation = Column(Boolean)
    raw_json_payload = Column(Text)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

_api_key_header = APIKeyHeader(name="X-Audit-Token", auto_error=False)


def verify_token(token: str = Security(_api_key_header)) -> str:
    # auto_error=False so we control the status code and message precisely.
    # Starlette 1.1 changed auto_error=True to emit 401; test spec requires 403.
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    if token != API_TOKEN_SECRET:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return token


# ---------------------------------------------------------------------------
# Statistical engine
# ---------------------------------------------------------------------------

class StatisticalNonStationarityAuditor:
    def __init__(self, apply_detrending: bool = True, bootstrap_iterations: int = 500):
        self.apply_detrending = apply_detrending
        self.bootstrap_iterations = bootstrap_iterations

    def _detrend_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Remove linear trend from each row via least-squares fit."""
        return signal.detrend(matrix, axis=1, type="linear")

    def calculate_bootstrap_p_value(
        self,
        matrix: np.ndarray,
        bootstrap_iterations: int = 500,
    ) -> tuple:
        """
        Bootstrap test for variance non-stationarity.

        Returns (observed_variance, empirical_p_value, null_distribution_stats).
        observed_variance: mean row-wise variance after optional detrending.
        empirical_p_value: fraction of null samples >= observed_variance.
        null_distribution_stats: dict with null_mean, null_ci_2_5, null_ci_97_5.
        """
        m = self._detrend_matrix(matrix) if self.apply_detrending else matrix
        observed_variance = float(np.mean(np.var(m, axis=1)))

        rng = np.random.default_rng()
        null_variances: List[float] = []
        for _ in range(bootstrap_iterations):
            shuffled = np.apply_along_axis(rng.permutation, axis=1, arr=m)
            null_variances.append(float(np.mean(np.var(shuffled, axis=1))))

        null_arr = np.array(null_variances)
        empirical_p_value = float(np.mean(null_arr >= observed_variance))

        null_dist_stats = {
            "null_mean":     float(np.mean(null_arr)),
            "null_ci_2_5":   float(np.percentile(null_arr, 2.5)),
            "null_ci_97_5":  float(np.percentile(null_arr, 97.5)),
        }

        return observed_variance, empirical_p_value, null_dist_stats


# ---------------------------------------------------------------------------
# Pydantic schema
# ---------------------------------------------------------------------------

class MatrixAuditRequest(BaseModel):
    url: str
    matrix_data: List[List[float]]
    bootstrap_iterations: int = 500
    apply_detrending: bool = True


# ---------------------------------------------------------------------------
# Persistence helper
# ---------------------------------------------------------------------------

def _persist_audit(db: Session, request: MatrixAuditRequest, result: tuple) -> None:
    observed_variance, empirical_p_value, null_dist_stats = result
    is_significant = empirical_p_value < 0.05

    payload = {
        "source_url": request.url,
        "statistical_results": {
            "observed_variance": observed_variance,
            "empirical_p_value": empirical_p_value,
            "null_distribution": null_dist_stats,
            "is_significant_tti_violation": is_significant,
        },
        "analysis_metadata": {
            "bootstrap_iterations": request.bootstrap_iterations,
            "apply_detrending": request.apply_detrending,
        },
    }

    log = NonStationaryAuditLog(
        source_url=request.url,
        observed_variance=observed_variance,
        empirical_p_value=empirical_p_value,
        is_significant_tti_violation=is_significant,
        raw_json_payload=json.dumps(payload),
    )
    db.add(log)
    db.commit()
    db.refresh(log)


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(title="MWS Non-Stationary Auditor v5")


@app.post("/api/v1/audit/matrix-stationarity", status_code=202)
async def audit_matrix_stationarity(
    request: MatrixAuditRequest,
    background_tasks: BackgroundTasks,
    token: str = Security(verify_token),
    db: Session = Depends(get_db),
):
    matrix = np.array(request.matrix_data)
    auditor = StatisticalNonStationarityAuditor(
        apply_detrending=request.apply_detrending,
        bootstrap_iterations=request.bootstrap_iterations,
    )
    result = auditor.calculate_bootstrap_p_value(matrix, request.bootstrap_iterations)

    # Persist synchronously within the active DB session.
    # Background task pattern is preserved for callers that extend this endpoint,
    # but writing in-handler avoids session lifecycle issues with TestClient.
    _persist_audit(db, request, result)

    observed_variance, empirical_p_value, _ = result
    return {
        "status": "accepted",
        "source_url": request.url,
        "observed_variance": observed_variance,
        "empirical_p_value": empirical_p_value,
        "is_significant_tti_violation": empirical_p_value < 0.05,
    }
