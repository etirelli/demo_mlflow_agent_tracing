FROM quay.io/sclorg/python-312-c10s:latest as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

USER 1001

WORKDIR /opt/app-root/src

# Install dependencies
COPY --chown=1001:0 pyproject.toml .python-version ./
COPY --chown=1001:0 uv.lock ./
RUN uv sync --no-install-project --no-editable --no-dev

# Install project
COPY --chown=1001:0 . .
RUN uv sync --no-dev

EXPOSE 8000

CMD [ "uv", "run", "--no-sync", "chainlit", "run", "src/demo_mlflow_agent_tracing/app.py", "--host", "0.0.0.0", "--port", "8000" ]
