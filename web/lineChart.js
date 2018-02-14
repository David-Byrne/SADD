'use strict';

/* global Chart:false */

class LineChart { // eslint-disable-line no-unused-vars
    constructor(canvas, topic1, topic2) {
        const defaultLen = Math.ceil((new Date() - new Date(2017, 10, 8)) / (24 * 60 * 60 * 1000));
        // defaultLen is roughly how many days of data we'll be displaying, since the animation
        // works best if we've about the same amount of place holder and real data.

        const chartConfig = {
            type: 'line',
            data: {
                labels: Array(defaultLen).fill('                  '),
                datasets: [{
                    label: topic1.name,
                    backgroundColor: topic1.colour,
                    borderColor: topic1.colour,
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: Array(defaultLen).fill(0),
                    fill: false,
                }, {
                    label: topic2.name,
                    backgroundColor: topic2.colour,
                    borderColor: topic2.colour,
                    borderWidth: 2.5,
                    pointRadius: 1,
                    data: Array(defaultLen).fill(0),
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
                    text: 'Mood',
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
                            min: -1,
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '):               Mood               (:',
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
            const scaledData = LineChart.scaleData(repealData);
            this.chart.config.data.datasets[0].data = scaledData;
        }
        if (saveData) {
            const scaleData = LineChart.scaleData(saveData);
            this.chart.config.data.datasets[1].data = scaleData;
        }

        this.chart.update();
    }

    static scaleData(data) {
        // Scales data to range [-1,1] instead of [0,1]
        return data.map(value => ((2 * value) - 1).toFixed(3));
    }
}
