'use strict';

/* global window:false document:false CONFIG:false WebSocket:false SentiCloud:false
          LineChart:false */
/* eslint-disable indent */ // Stops eslint complaining about indentation in switch statement

function sortObjectKeys(object) {
    const orderedObject = {};
    Object.keys(object).sort().forEach((key) => {
        orderedObject[key] = object[key];
    });
    return orderedObject;
}

window.onload = () => {
    document.getElementById('website-name').innerText = CONFIG.name;

    const lc = new LineChart(document.getElementById('sentiment-graph'), CONFIG.topic1, CONFIG.topic2);
    const repealCloud = new SentiCloud(CONFIG.topic1.name, document.getElementById('repeal-cloud'), {
        backgroundColor: CONFIG.topic1.colour,
    });
    const saveCloud = new SentiCloud(CONFIG.topic2.name, document.getElementById('save-cloud'), {
        backgroundColor: CONFIG.topic2.colour,
    });

    const socket = new WebSocket(`ws://${window.location.hostname}:8080`);

    socket.onopen = () => {
        console.log('Connection established');
        document.getElementById('loading-bar').classList.remove('loader-bar');
    };

    socket.onmessage = (message) => {
        const data = JSON.parse(message.data);

        switch (data.channel) {
            case 'vp:senti': {
                const orderedData = sortObjectKeys(data.data);
                lc.updateGraph(Object.keys(orderedData), null, Object.values(orderedData));
                break;
            }
            case 'vn:senti': {
                const orderedData = sortObjectKeys(data.data);
                lc.updateGraph(Object.keys(orderedData), Object.values(orderedData), null);
                break;
            }
            case 'vp:cloud': {
                repealCloud.updateGraph(Object.entries(data.data));
                break;
            }
            case 'vn:cloud': {
                saveCloud.updateGraph(Object.entries(data.data));
                break;
            }
            default: {
                break;
            }
        }
    };
};
