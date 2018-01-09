'use strict';

/* global Chart:false */

class LineChart { // eslint-disable-line no-unused-vars
    constructor(canvas, labels, saveData, repealData) {
        const chartConfig = {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: '#RepealThe8th',
                    backgroundColor: 'rgb(0, 0, 0)',
                    borderColor: 'rgb(0, 0, 0)',
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: repealData,
                    fill: false,
                }, {
                    label: '#SaveThe8th',
                    backgroundColor: 'rgb(237, 32, 123)',
                    borderColor: 'rgb(237, 32, 123)',
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: saveData,
                    fill: false,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Sentiment Chart [**FAKE DATA**]',
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
        this.chart.config.data.datasets[0].data = repealData;
        this.chart.config.data.datasets[1].data = saveData;
        this.chart.update();
    }
}
