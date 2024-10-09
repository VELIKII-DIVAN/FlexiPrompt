# this is container for run tests
FROM python:3.12-slim

WORKDIR /app


COPY ../flexi_prompt/ .


# RUN pip install --no-cache-dir poetry
RUN pip install --no-cache-dir hatch

# COPY ./pyproject.toml .

COPY . .

RUN ls -l

RUN hatch build


ENV PYTHONPATH=/app/flexi_prompt

CMD ["pytest", "tests", "-v"]