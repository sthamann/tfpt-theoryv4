# TFPT — a runnable image of the reality compiler.
#
#   docker build -t tfpt .
#   docker run --rm tfpt                 # 30-second headline verification
#   docker run --rm tfpt --full          # the whole Python suite
#
# Or pull the published image (no local build):
#   docker run --rm ghcr.io/sthamann/tfpt:latest
#
# The image carries only the Python verification stack (mpmath, numpy, sympy,
# matplotlib) — no LaTeX, Wolfram or Lean — so `./verify` and `./verify --full`
# run out of the box.  The optional second/third engines live outside the image.
FROM python:3.12-slim

LABEL org.opencontainers.image.title="TFPT — Topological Fixed-Point Theory"
LABEL org.opencontainers.image.description="A parameter-free discrete compiler for the dimensionless Standard-Model skeleton; every load-bearing claim machine-checked."
LABEL org.opencontainers.image.source="https://github.com/sthamann/tfpt"
LABEL org.opencontainers.image.licenses="see repository"

WORKDIR /tfpt

# Dependencies first, so the layer caches across source edits.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only what the verifier needs at runtime.
COPY verify ./verify
COPY verification ./verification

ENTRYPOINT ["./verify"]
CMD []
