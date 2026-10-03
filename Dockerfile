# syntax=docker/dockerfile:1.6
# Production image for canvas_security scanning platform.
# tini is the PID-1 init: it propagates SIGTERM into the scanner process
# and reaps zombie children, complementing the SIGKILL escalation that
# ContainerizedScannerConnector uses via os.killpg.

# ── build stage ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS build

WORKDIR /build

# canvas_security's only runtime dependency is psutil.
# Isolated prefix means nothing leaks into the final stage unexpectedly.
COPY canvas_security.py .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/install --no-compile psutil==5.9.8

# ── runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Install tini from a pinned release with SHA-256 verification.
# tini -g forwards signals to the full child process group, which mirrors
# how canvas_security terminates timed-out scans with os.killpg.
ARG TINI_VERSION=v0.19.0
ARG TINI_SHA256=93dcc18adc78c65a028a84799ecf8ad40c936fdfc5f2a57b1acda5a8117fa82c
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -fsSL \
        "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64" \
        -o /usr/local/bin/tini && \
    echo "${TINI_SHA256}  /usr/local/bin/tini" | sha256sum -c - && \
    chmod +x /usr/local/bin/tini && \
    apt-get purge -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy installed wheels from build stage
COPY --from=build /install /usr/local

# Least-privilege runtime user; scanner never needs a home directory or login
RUN groupadd --gid 10001 scanner && \
    useradd  --uid 10001 --gid scanner \
             --no-create-home --shell /sbin/nologin scanner

WORKDIR /app

COPY canvas_security.py .

# Lock down the working directory
RUN chown -R scanner:scanner /app && chmod -R o-w /app

USER scanner

# Health metadata
LABEL org.opencontainers.image.title="canvas-security-scanner" \
      org.opencontainers.image.description="Containerized security scanning platform with process isolation" \
      org.opencontainers.image.version="1.0.0"

# tini -g: signal the child's entire process group on SIGTERM/SIGINT,
# consistent with ContainerizedScannerConnector's os.killpg escalation.
ENTRYPOINT ["/usr/local/bin/tini", "-g", "--"]

# Override CMD with the actual scanner entry point at deployment time.
# Example: docker run canvas-scanner python -m myapp.scanner --target 10.0.0.0/24
CMD ["python", "-c", "from canvas_security import EnhancedSecurityPlatform; print('canvas_security ready')"]
