"""
Universal Request Filter Middleware
- Profanity filtering
- PII redaction (credit cards, SSN, emails)
- JSON conversion (plain text -> JSON)
- Rate limiting by content type
- Logging and auditing
"""

import re
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, List, Optional, Callable


class SmartFilterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        enable_profanity_filter: bool = True,
        enable_pii_redaction: bool = True,
        enable_json_wrapper: bool = False,
        rate_limit: Optional[int] = None,  # requests per minute per IP
        log_file: Optional[str] = None,
        custom_filters: Optional[List[Callable]] = None
    ):
        super().__init__(app)
        self.enable_profanity_filter = enable_profanity_filter
        self.enable_pii_redaction = enable_pii_redaction
        self.enable_json_wrapper = enable_json_wrapper
        self.rate_limit = rate_limit
        self.log_file = log_file
        self.custom_filters = custom_filters or []

        self.profanity_pattern = re.compile(
            r'\b(fuck|shit|damn|bitch|cunt|asshole|bastard)\b',
            re.IGNORECASE
        )

        self.pii_patterns = {
            'email':       re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b'),
            'credit_card': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
            'ssn':         re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'phone':       re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
        }

        self.request_counts: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        content_type = request.headers.get("content-type", "")
        if "text/plain" not in content_type and "application/json" not in content_type:
            return await call_next(request)

        # Rate limiting
        if self.rate_limit:
            client_ip = request.client.host
            now = time.time()
            window_start = now - 60
            self.request_counts.setdefault(client_ip, [])
            self.request_counts[client_ip] = [
                t for t in self.request_counts[client_ip] if t > window_start
            ]
            if len(self.request_counts[client_ip]) >= self.rate_limit:
                return Response("Rate limit exceeded", status_code=429)
            self.request_counts[client_ip].append(now)

        body = await request.body()
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            return await call_next(request)

        original_text = text

        if self.enable_profanity_filter:
            text = self.profanity_pattern.sub("[redacted]", text)

        if self.enable_pii_redaction:
            for name, pattern in self.pii_patterns.items():
                text = pattern.sub(f"[{name}_redacted]", text)

        for filt in self.custom_filters:
            text = filt(text)

        if self.enable_json_wrapper and not text.strip().startswith('{'):
            import json
            text = json.dumps({"message": text})

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(f"{time.ctime()} | {request.client.host} | {request.method} {request.url.path}\n")
                f.write(f"  Original: {original_text[:200]}\n")
                f.write(f"  Filtered: {text[:200]}\n\n")

        async def receive():
            return {"type": "http.request", "body": text.encode()}

        new_scope = dict(request.scope)
        new_scope["headers"] = [(b"content-type", b"text/plain")]
        new_request = Request(new_scope, receive=receive)
        return await call_next(new_request)
