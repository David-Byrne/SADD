FROM node:8.9.4
COPY . /websocket
WORKDIR /websocket
EXPOSE 8080
RUN npm install
CMD ["node", "websocket.js"]
