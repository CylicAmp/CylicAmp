"""
SovereignKernel v3 — deterministic execution runtime with append-only ledger.

Architecture:
  StorageModule  — SQLite-backed axiom versioning, manifest registry, ledger
  PipelineModule — engine registry, deterministic execution, hash-chain
  FastAPI layer  — REST interface to all subsystems

Key properties:
  - Axiom lineage: every logic version is retained, never overwritten
  - Manifest immutability: registered manifests cannot be silently replaced
  - State chaining: each tx records (prev_hash → tx_hash) for chain verification
  - Durable chain: on startup, state is recovered from the latest ledger row
  - Canonical hashing: json.dumps(sort_keys=True, separators=(',',':'))
  - WAL mode: concurrent reads + writes without locking errors

Requires: fastapi, uvicorn  (pip install fastapi uvicorn)
"""

import hashlib
import json
import sqlite3
import threading
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# =============================================================================
# StorageModule
# =============================================================================

class StorageModule:
    INIT_HASH = hashlib.sha256(b"SOVEREIGN_KERNEL_V3_INIT").hexdigest()

    def __init__(self, db_path: str = "kernel_v3.db"):
        self.db = db_path
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db, timeout=30)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS axioms (
                    key          TEXT    NOT NULL,
                    version      INTEGER NOT NULL,
                    value        TEXT    NOT NULL,
                    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (key, version)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS manifests (
                    manifest_id  TEXT PRIMARY KEY,
                    engine       TEXT NOT NULL,
                    axiom_key    TEXT NOT NULL,
                    input_schema TEXT NOT NULL,
                    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Full hash-chain ledger: each row is self-describing for replay.
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ledger (
                    tx_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    tx_hash        TEXT NOT NULL,
                    prev_hash      TEXT NOT NULL,
                    manifest_id    TEXT NOT NULL,
                    engine_name    TEXT NOT NULL,
                    axiom_key      TEXT NOT NULL,
                    axiom_version  INTEGER NOT NULL,
                    input_hash     TEXT NOT NULL,
                    result_hash    TEXT NOT NULL,
                    payload        TEXT NOT NULL,
                    schema_version INTEGER DEFAULT 1,
                    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    # ------------------------------------------------------------------
    # Axioms
    # ------------------------------------------------------------------

    def write_axiom(self, key: str, value: str) -> dict:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT MAX(version) FROM axioms WHERE key=?", (key,)
            ).fetchone()
            next_version = (row[0] or 0) + 1
            conn.execute(
                "INSERT INTO axioms (key, version, value) VALUES (?, ?, ?)",
                (key, next_version, value),
            )
        return {"status": "AXIOM_COMMITTED", "key": key, "version": next_version}

    def read_axiom(self, key: str, version: Optional[int] = None) -> Optional[tuple]:
        with self._connect() as conn:
            if version is not None:
                return conn.execute(
                    "SELECT value, version FROM axioms WHERE key=? AND version=?",
                    (key, version),
                ).fetchone()
            return conn.execute(
                "SELECT value, version FROM axioms WHERE key=? ORDER BY version DESC LIMIT 1",
                (key,),
            ).fetchone()

    # ------------------------------------------------------------------
    # Manifests — immutable after first registration
    # ------------------------------------------------------------------

    def write_manifest(
        self, manifest_id: str, engine: str, axiom_key: str, input_schema: dict
    ) -> dict:
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT manifest_id FROM manifests WHERE manifest_id=?", (manifest_id,)
            ).fetchone()
            if existing:
                raise ValueError(f"MANIFEST_EXISTS: {manifest_id} is immutable once registered")
            conn.execute(
                "INSERT INTO manifests (manifest_id, engine, axiom_key, input_schema) VALUES (?, ?, ?, ?)",
                (manifest_id, engine, axiom_key, json.dumps(input_schema)),
            )
        return {"status": "MANIFEST_STORED", "manifest_id": manifest_id}

    def get_manifest(self, manifest_id: str) -> Optional[tuple]:
        with self._connect() as conn:
            return conn.execute(
                "SELECT engine, axiom_key FROM manifests WHERE manifest_id=?",
                (manifest_id,),
            ).fetchone()

    # ------------------------------------------------------------------
    # Ledger
    # ------------------------------------------------------------------

    def append_ledger(
        self,
        tx_hash: str,
        prev_hash: str,
        manifest_id: str,
        engine_name: str,
        axiom_key: str,
        axiom_version: int,
        input_hash: str,
        result_hash: str,
        payload: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO ledger
                   (tx_hash, prev_hash, manifest_id, engine_name, axiom_key,
                    axiom_version, input_hash, result_hash, payload)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (tx_hash, prev_hash, manifest_id, engine_name, axiom_key,
                 axiom_version, input_hash, result_hash, payload),
            )

    def get_ledger(self, limit: int = 100) -> list:
        limit = min(limit, 1000)
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM ledger ORDER BY tx_id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_ledger_row(self, tx_id: int) -> Optional[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM ledger WHERE tx_id=?", (tx_id,)
            ).fetchone()
            return dict(row) if row else None

    def recover_latest_tx_hash(self) -> str:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT tx_hash FROM ledger ORDER BY tx_id DESC LIMIT 1"
            ).fetchone()
        return row[0] if row else self.INIT_HASH


# =============================================================================
# PipelineModule
# =============================================================================

def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class PipelineModule:
    def __init__(self, storage: StorageModule):
        self.storage = storage
        self.registry: Dict[str, Any] = {}
        self._lock = threading.Lock()
        # Recover durable chain state from ledger on startup.
        self.global_state_hash = storage.recover_latest_tx_hash()

    def register_engine(self, engine_name: str, func) -> None:
        self.registry[engine_name] = func

    def execute_manifest(self, manifest_id: str, data: Dict[str, Any]) -> dict:
        manifest = self.storage.get_manifest(manifest_id)
        if not manifest:
            raise ValueError("MANIFEST_NOT_FOUND")

        engine_name, axiom_key = manifest
        axiom_record = self.storage.read_axiom(axiom_key)
        if not axiom_record:
            raise ValueError("AXIOM_NOT_FOUND")

        axiom_data, axiom_version = axiom_record
        engine = self.registry.get(engine_name)
        if not engine:
            raise ValueError(f"ENGINE_NOT_FOUND: {engine_name}")

        result = engine(axiom_data, data)

        input_hash  = hashlib.sha256(_canonical(data).encode()).hexdigest()
        result_hash = hashlib.sha256(_canonical(result).encode()).hexdigest()

        with self._lock:
            prev_hash = self.global_state_hash
            chain_payload = {
                "prev_hash":     prev_hash,
                "manifest_id":   manifest_id,
                "engine_name":   engine_name,
                "axiom_key":     axiom_key,
                "axiom_version": axiom_version,
                "input_hash":    input_hash,
                "result_hash":   result_hash,
            }
            tx_hash = hashlib.sha256(_canonical(chain_payload).encode()).hexdigest()
            self.global_state_hash = tx_hash

        self.storage.append_ledger(
            tx_hash=tx_hash,
            prev_hash=prev_hash,
            manifest_id=manifest_id,
            engine_name=engine_name,
            axiom_key=axiom_key,
            axiom_version=axiom_version,
            input_hash=input_hash,
            result_hash=result_hash,
            payload=_canonical(chain_payload),
        )

        return {"result": result, "tx_hash": tx_hash}

    def replay_tx(self, tx_id: int) -> dict:
        """Recompute tx_hash from stored payload and compare to ledger."""
        row = self.storage.get_ledger_row(tx_id)
        if not row:
            raise ValueError(f"TX_NOT_FOUND: {tx_id}")
        recomputed = hashlib.sha256(row["payload"].encode()).hexdigest()
        stored     = row["tx_hash"]
        return {
            "tx_id":       tx_id,
            "stored_hash": stored,
            "recomputed":  recomputed,
            "valid":       recomputed == stored,
        }


# =============================================================================
# Kernel assembly
# =============================================================================

class SovereignKernelV3:
    def __init__(self, db_path: str = "kernel_v3.db"):
        self.storage  = StorageModule(db_path)
        self.pipeline = PipelineModule(self.storage)


kernel = SovereignKernelV3()
app    = FastAPI(title="SovereignKernel_v3")


# =============================================================================
# Pydantic schemas
# =============================================================================

class ManifestPayload(BaseModel):
    manifest_id:  str
    engine:       str
    axiom_key:    str
    input_schema: Dict[str, Any]

class ExecutionPayload(BaseModel):
    manifest_id: str
    data:        Dict[str, Any]


# =============================================================================
# API endpoints
# =============================================================================

@app.post("/storage/axiom/write")
async def write_axiom(key: str, value: str):
    return kernel.storage.write_axiom(key, value)

@app.get("/storage/axiom/read")
async def read_axiom(key: str, version: Optional[int] = None):
    record = kernel.storage.read_axiom(key, version)
    if not record:
        raise HTTPException(status_code=404, detail="AXIOM_NOT_FOUND")
    return {"key": key, "version": record[1], "value": record[0]}

@app.post("/kernel/manifest/register")
async def register_manifest(payload: ManifestPayload):
    try:
        return kernel.storage.write_manifest(
            payload.manifest_id, payload.engine, payload.axiom_key, payload.input_schema
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.post("/kernel/engine/bind")
async def bind_engine(engine_name: str, logic_type: str):
    def engine_logic(axiom, data):
        return {"derivation": f"{logic_type}_EXECUTION", "axiom_state": axiom, "input": data}
    kernel.pipeline.register_engine(engine_name, engine_logic)
    return {"status": "ENGINE_BOUND", "engine": engine_name}

@app.post("/kernel/pipeline/execute")
async def run_pipeline(payload: ExecutionPayload):
    try:
        return kernel.pipeline.execute_manifest(payload.manifest_id, payload.data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ledger/audit")
async def audit_ledger(limit: int = 100):
    return {"ledger": kernel.storage.get_ledger(limit)}

@app.get("/ledger/replay/{tx_id}")
async def replay_tx(tx_id: int):
    try:
        return kernel.pipeline.replay_tx(tx_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
