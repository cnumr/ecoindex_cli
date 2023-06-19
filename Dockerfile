# Build image
FROM python:3.11-slim as requirements-stage

ARG CHROME_VERSION_MAIN=111

WORKDIR /tmp

# Install required deps
RUN apt update && apt install -y unzip wget

# Download chromedriver and chrome
RUN wget "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION_MAIN}" -O /tmp/chrome_version
RUN wget "https://chromedriver.storage.googleapis.com/$(cat /tmp/chrome_version)/chromedriver_linux64.zip" \
    && unzip -o chromedriver_linux64.zip
RUN wget "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$(cat /tmp/chrome_version)-1_amd64.deb" \
    -O google-chrome-stable.deb

# Build ecoindex-cli
COPY ./ ./
RUN pip install poetry
RUN poetry build

# Main image
FROM python:3.11-slim

ARG CHROME_VERSION_MAIN=111
ENV CHROME_VERSION_MAIN=${CHROME_VERSION_MAIN}
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /code

# Copy built packages, chromedriver, google-chrome-stable.deb from requirements-stage
COPY --from=requirements-stage /tmp/dist/ /tmp/dist/
COPY --from=requirements-stage /tmp/chromedriver /usr/bin/chromedriver
COPY --from=requirements-stage /tmp/google-chrome-stable.deb /tmp/

# Install google chrome and make chromedriver executable
RUN apt update && apt -y install libpq-dev gcc /tmp/google-chrome-stable.deb
RUN chmod +x /usr/bin/chromedriver

# Install ecoindex-cli
RUN pip install /tmp/dist/*.whl

# Clean up
RUN rm -rf /tmp/google-chrome-stable.deb /tmp/dist /var/lib/{apt,dpkg,cache,log}/
