# Build image
FROM python:3.11-slim AS requirements-stage

ARG CHROME_VERSION_MAIN=108
ENV CHROME_VERSION_MAIN=${CHROME_VERSION_MAIN}

WORKDIR /tmp

# Install required deps
RUN apt-get update && apt-get install -y unzip
RUN pip install poetry tqdm requests pydantic

# Download chromedriver and chrome
COPY ./scripts/download_chrome.py download_chrome.py
RUN python download_chrome.py --main-version ${CHROME_VERSION_MAIN} \
    --chrome-filename /tmp/chrome.zip \
    --chromedriver-filename /tmp/chromedriver.zip
RUN unzip -j /tmp/chromedriver.zip -d /tmp
RUN unzip -j /tmp/chrome.zip -d /tmp/chrome
COPY ./ ./
RUN pip install poetry
RUN poetry build

# Main image
FROM python:3.11-slim

ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /code
ENV PYTHONPATH "/code"
ENV CHROME_EXECUTABLE_PATH "/opt/chrome/chrome"
ENV CHROME_VERSION_MAIN 108

RUN apt update && apt install -y ca-certificates fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 \
    libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 \
    libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
    libxss1 libxtst6 lsb-release wget xdg-utils

# Copy requirements.txt, chromedriver, chrome from requirements-stage
COPY --from=requirements-stage /tmp/dist/ /tmp/dist/
COPY --from=requirements-stage /tmp/chromedriver ${CHROMEDRIVER_PATH}
COPY --from=requirements-stage /tmp/chrome /opt/chrome

# Install google chrome and make chromedriver executable
RUN chmod +x ${CHROMEDRIVER_PATH}

# Install ecoindex-cli
RUN pip install /tmp/dist/*.whl

# Clean up
RUN rm -rf /tmp/dist /var/lib/{apt,dpkg,cache,log}/
