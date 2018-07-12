FROM nginx:1.13.8
COPY web/frontend/ /usr/share/nginx/html
COPY config.json .
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# ensures piping works consistently by setting -o pipefall arg, see Hadolint DL4006
RUN printf 'const CONFIG=' | cat - config.json > /usr/share/nginx/html/config.js
# Converts config.json into a valid config.js
EXPOSE 80
