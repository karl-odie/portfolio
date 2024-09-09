FROM docker.io/node:22-bookworm-slim

WORKDIR /app

COPY ./package.json /app

RUN apt-get update && apt-get install -y \
    libgtk2.0-0 libgtk-3-0 libgbm-dev \
    libnotify-dev libnss3 libxss1 libasound2 \
    libxtst6 xauth xvfb \
    default-jre
RUN npm install && npm cache clean --force

ENV PATH=./node_modules/.bin/:$PATH
