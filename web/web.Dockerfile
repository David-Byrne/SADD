FROM nginx:1.13.8
COPY web/frontend/ /usr/share/nginx/html
COPY config.json .
RUN echo -n 'const CONFIG=' | cat - config.json > /usr/share/nginx/html/config.js
# Converts config.json into a valid config.js
EXPOSE 80
