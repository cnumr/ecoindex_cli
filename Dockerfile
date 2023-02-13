FROM python:3.11-slim as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./ ./
RUN poetry build

FROM python:3.11-slim
ARG CHROME_VERSION=107.0.5304.121-1
ENV CHROME_VERSION=$CHROME_VERSION
WORKDIR /code
RUN apt-get update && apt-get -y install libpq-dev gcc wget
RUN wget "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb" \
    && apt-get install -y "./google-chrome-stable_${CHROME_VERSION}_amd64.deb" \
    && rm "google-chrome-stable_${CHROME_VERSION}_amd64.deb"
COPY --from=requirements-stage /tmp/dist/ /tmp/dist/
RUN pip install /tmp/dist/*.whl