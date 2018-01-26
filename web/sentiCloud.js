'use strict';

/* global WordCloud:false */

class SentiCloud { // eslint-disable-line no-unused-vars
    constructor(element, extraConfig) {
        const defaultConfig = {
            fontFamily: 'Helvetica',
            color: '#ffffff',
            rotateRatio: 0.0,
            rotationSteps: 2,
            shuffle: 0,
            wait: 10,
            weightFactor: 1,
            gridSize: 12,
            classes: 'cloud-word',
        };

        this.config = Object.assign(defaultConfig, extraConfig);
        this.config.list = [];
        this.element = element;
        WordCloud(element, this.config);
    }

    updateGraph(data) {
        // Maybe run a check first to see if the update would actually change things?
        data.sort((a, b) => b[1] - a[1]);

        if (this.isWorthRepaint(data)) {
            const scaledWords = data.map(entry => [entry[0], 6 * Math.log(entry[1] / 1.3)]);
            this.config.list = scaledWords;
            WordCloud(this.element, this.config);
        }
    }

    isWorthRepaint(data) {
        if (data.length !== this.config.list.length) {
            return true;
        }

        let diffCounter = 0;

        for (const [index, pair] of data.entries()) {
            if (pair[0] !== this.config.list[index][0]) {
                diffCounter++;
            }
        }

        return diffCounter > 10;
        // Any fewer changes than that and it's not really worth a repaint...
    }
}
