'use strict';

const ws = require('ws');
const bluebird = require('bluebird');
const redis = require('redis');

bluebird.promisifyAll(redis.RedisClient.prototype);


class WebSocket {
    constructor() {
        this.KEYS = ['vp:senti', 'vn:senti'];
        // TODO: Add in expected datatype, for now we're just assuming it's a hashmap
        this.wsServer = new ws.Server({ port: 8080 });
        this.redisCon = redis.createClient();
        this.redisSub = redis.createClient();
    }

    listen() {
        // Listen for new Websocket Connections
        this.wsServer.on('connection', (socket) => {
            this.sendLatestData(socket);
        });

        // When there's been a Redis update
        this.redisSub.on('message', (channel) => {
            const key = WebSocket.getRedisKey(channel);

            this.redisCon.hgetallAsync(key)
                .then((resp) => {
                    const data = WebSocket.formatDataForSending(key, resp);
                    this.broadcastUpdates(data);
                })
                .catch(console.error);
        });

        // Listen for Redis updates
        for (const key of this.KEYS) {
            this.redisSub.subscribe(`__keyspace@0__:${key}`);
        }
    }

    broadcastUpdates(data) {
        this.wsServer.clients.forEach((client) => {
            if (client.readyState === ws.OPEN) {
                client.send(data);
            }
        });
    }

    sendLatestData(socket) {
        for (const key of this.KEYS) {
            this.redisCon.hgetallAsync(key)
                .then((resp) => {
                    const data = WebSocket.formatDataForSending(key, resp);
                    socket.send(data);
                })
                .catch(console.error);
        }
    }

    static getRedisKey(channel) {
        const offset = '__keyspace@0__:'.length;
        return channel.slice(offset);
    }

    static formatDataForSending(channel, data) {
        const resp = {
            channel,
            data,
        };
        return JSON.stringify(resp);
    }
}

const socket = new WebSocket();
socket.listen();
