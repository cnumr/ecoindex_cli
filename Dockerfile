# Build image
FROM python:3.11-slim as requirements-stage

ARG CHROME_VERSION_MAIN=111

WORKDIR /tmp
COPY ./ ./

# Install required deps
RUN apt update && apt install -y unzip wget
RUN pip install poetry
RUN poetry build

# Build requirements.txt file
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export --with=worker --output=requirements.txt --without-hashes

# Download chromedriver and chrome
RUN wget "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION_MAIN}" -O /tmp/chrome_version
RUN wget "https://chromedriver.storage.googleapis.com/$(cat /tmp/chrome_version)/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip
RUN wget "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$(cat /tmp/chrome_version)-1_amd64.deb" \
    && mv "google-chrome-stable_$(cat /tmp/chrome_version)-1_amd64.deb" google-chrome-stable.deb


# Main image
FROM python:3.11-slim

ARG CHROME_VERSION_MAIN=111
ENV CHROME_VERSION_MAIN=${CHROME_VERSION_MAIN}
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /code

# Copy requirements.txt, chromedriver, chrome_version, google-chrome-stable.deb from requirements-stage
COPY --from=requirements-stage /tmp/dist/ /tmp/dist/
COPY --from=requirements-stage /tmp/chromedriver /usr/bin/chromedriver
COPY --from=requirements-stage /tmp/chrome_version /tmp/chrome_version
COPY --from=requirements-stage /tmp/google-chrome-stable.deb /tmp/

# Install google chrome and make chromedriver executable
RUN apt update && apt -y install libpq-dev gcc /tmp/google-chrome-stable.deb
RUN chmod +x /usr/bin/chromedriver

RUN pip install /tmp/dist/*.whl