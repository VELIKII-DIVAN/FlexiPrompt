FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml  flexi_prompt/  tests/   README.md  ./


RUN pip install --no-cache-dir .[test]

CMD ["pytest"]