'use strict';

/* global Chart:false */

class LineChart { // eslint-disable-line no-unused-vars
    constructor(canvas) {
        const defaultLen = Math.ceil((new Date() - new Date(2017, 10, 8)) / (24 * 60 * 60 * 1000));
        // defaultLen is roughly how many days of data we'll be displaying, since the animation
        // works best if we've about the same amount of place holder and real data.

        const chartConfig = {
            type: 'line',
            data: {
                labels: Array(defaultLen).fill('                  '),
                datasets: [{
                    label: '#RepealThe8th',
                    backgroundColor: 'rgb(0, 0, 0)',
                    borderColor: 'rgb(0, 0, 0)',
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: Array(defaultLen).fill(0.5),
                    fill: false,
                }, {
                    label: '#SaveThe8th',
                    backgroundColor: 'rgb(237, 32, 123)',
                    borderColor: 'rgb(237, 32, 123)',
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: Array(defaultLen).fill(0.5),
                    fill: false,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1500,
                },
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Sentiment Chart',
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true,
                },
                scales: {
                    xAxes: [{
                        display: true,
                        ticks: {
                            fontSize: 10,
                        },
                        scaleLabel: {
                            display: false,
                            labelString: 'Date',
                        },
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            max: 1,
                            min: 0,
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Sentiment',
                        },
                    }],
                },
            },
        };

        this.chart = new Chart(canvas, chartConfig);
    }

    updateGraph(labels, saveData, repealData) {
        this.chart.config.data.labels = labels;

        if (repealData) {
            this.chart.config.data.datasets[0].data = repealData;
        }
        if (saveData) {
            this.chart.config.data.datasets[1].data = saveData;
        }

        this.chart.update();
    }
}
