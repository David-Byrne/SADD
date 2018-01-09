"use strict";

class SentiCloud{

    constructor(element, data, extraConfig){
        const defaultConfig = {
            fontFamily: "Helvetica",
            rotateRatio: 0.0,
            rotationSteps: 2,
            shuffle: 0,
            wait: 10,
            weightFactor: 2,
            shape: "square",
            gridSize: 12,
            classes: "cloud-word"
        };

        this.config = Object.assign(defaultConfig, extraConfig);
        this.config["list"] = data;
        this.data = data;
        this.element = element;
        WordCloud(element, this.config);
    }

    updateGraph(data){
        // Maybe run a check first to see if the update would actually change things?
        const config = Object.assign(this.config, {list: data});
        WordCloud(this.element, this.config);
    }
}
