#!/usr/bin/env python3
"""
Client-side proof-of-work solver.

A client wanting to authenticate must:
1. Fetch a problem instance from the server
2. Solve it (may take 100-1000ms depending on difficulty)
3. Include the proof in the Authorization header of their request

Example:
    client = ProofOfWorkClient("http://localhost:8000")
    headers = await client.get_auth_headers("/api/protected-endpoint")
    response = await httpx.get("/api/protected-endpoint", headers=headers)
"""

import time
import asyncio
from typing import Optional, Dict
from dataclasses import asdict
import httpx

from .proof_of_work import (
    ProblemInstance,
    ProblemType,
    Proof,
    discrete_log,
    P
)

class ProofOfWorkClient:
    """Client that solves proof-of-work challenges."""

    def __init__(self, server_url: str, client_ip: Optional[str] = None):
        self.server_url = server_url.rstrip("/")
        self.client_ip = client_ip or "127.0.0.1"

    async def request_problem(self, path: str) -> Optional[ProblemInstance]:
        """
        Fetch a problem instance from the server.

        Server responds with JSON:
        {
            "problem_type": "dlog",
            "timestamp": 1728072345,
            "target": 18,
            "base": 2,
            "difficulty": 100,
            ...
        }
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.server_url}/proof-of-work/problem",
                    params={"path": path}
                )
                response.raise_for_status()

                data = response.json()
                return ProblemInstance(
                    problem_type=ProblemType(data["problem_type"]),
                    timestamp=data["timestamp"],
                    requester_ip=data["requester_ip"],
                    server_state_hash=data["server_state_hash"],
                    difficulty=data["difficulty"],
                    target=data["target"],
                    base=data.get("base", 2)
                )
        except Exception as e:
            print(f"Error fetching problem: {e}")
            return None

    def solve_discrete_log(self, problem: ProblemInstance) -> Optional[Proof]:
        """
        Solve a discrete-log problem: find x where base^x ≡ target (mod 37).

        Uses baby-step giant-step algorithm: O(sqrt(p)) time.
        For p=37, this is ~6 operations on average.

        With difficulty calibration, can be tuned to take 100-1000ms.
        """
        start = time.time()

        solution = discrete_log(problem.target, problem.base, P)
        if solution is None:
            return None

        elapsed_ms = int((time.time() - start) * 1000)

        return Proof(
            problem_hash=hash(problem),
            solution=solution,
            solve_time_ms=elapsed_ms,
            timestamp=int(time.time())
        )

    def solve_orbit_collision(self, problem: ProblemInstance) -> Optional[Proof]:
        """
        Solve an orbit collision problem: find cycle in f(n) = 26n mod 37.

        For the 137-map, all orbits have order 3, so this is trivial to find.
        Difficulty is calibrated by adding artificial delay.
        """
        start = time.time()

        f = lambda n: (26 * n) % P
        current = problem.target
        steps = []

        for i in range(P):  # Maximum possible cycle length
            steps.append(current)
            current = f(current)
            if current == problem.target:
                break

        elapsed_ms = int((time.time() - start) * 1000)

        # Calibrate: if solved too fast, add delay to match difficulty
        if elapsed_ms < problem.difficulty * 0.5:
            delay_ms = problem.difficulty - elapsed_ms
            time.sleep(delay_ms / 1000.0)
            elapsed_ms = problem.difficulty

        return Proof(
            problem_hash=hash(problem),
            solution=len(steps),  # Return cycle length
            solve_time_ms=elapsed_ms,
            timestamp=int(time.time())
        )

    def solve_problem(self, problem: ProblemInstance) -> Optional[Proof]:
        """Dispatch to the appropriate solver."""
        if problem.problem_type == ProblemType.DISCRETE_LOG:
            return self.solve_discrete_log(problem)
        elif problem.problem_type == ProblemType.ORBIT_COLLISION:
            return self.solve_orbit_collision(problem)
        else:
            raise ValueError(f"Unknown problem type: {problem.problem_type}")

    def proof_to_headers(self, proof: Proof) -> Dict[str, str]:
        """Convert proof to HTTP headers."""
        return {
            "X-Proof-Hash": str(proof.problem_hash),
            "X-Solution": str(proof.solution),
            "X-Solve-Time": str(proof.solve_time_ms),
        }

    async def get_auth_headers(self, path: str) -> Optional[Dict[str, str]]:
        """
        Full flow: fetch problem, solve it, return authorization headers.

        This is what a client does before making a protected request.
        """
        print(f"[PoW Client] Requesting problem for {path}...")
        problem = await self.request_problem(path)
        if not problem:
            return None

        print(f"[PoW Client] Problem: {problem}")
        print(f"[PoW Client] Solving (target solve time: {problem.difficulty}ms)...")

        proof = self.solve_problem(problem)
        if not proof:
            print(f"[PoW Client] Failed to solve problem")
            return None

        print(f"[PoW Client] Solved in {proof.solve_time_ms}ms")
        return self.proof_to_headers(proof)

# ============================================================================
# Example Usage (synchronous wrapper for scripts)
# ============================================================================

def solve_problem_sync(server_url: str, path: str) -> Optional[Dict[str, str]]:
    """Synchronous wrapper for getting auth headers."""
    client = ProofOfWorkClient(server_url)
    return asyncio.run(client.get_auth_headers(path))
