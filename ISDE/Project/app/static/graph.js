$(document).ready(function () {
    var scripts = document.getElementById('makeGraph');
    var classification_scores = scripts.getAttribute('classification_scores');
    makeGraph(classification_scores);
});

/**
 * Generates a horizontal bar chart displaying classification results using Chart.js.
 *
 * This function takes classification results as input, parses them if they are in JSON format,
 * and visualizes them as a horizontal bar chart using Chart.js.
 *
 * @param {string | array} results - A JSON string or an array containing classification results.
 * @throws {Error} If results are not in a valid JSON format.
 */
function makeGraph(results) {
    console.log(results);
    
    try {
        results = JSON.parse(results);
    } catch (error) {
        console.error("Error parsing classification results:", error);
        return;
    }

    var ctx = document.getElementById("classification_output").getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: results.map(item => item[0]), // Extract labels dynamically
            datasets: [{
                label: 'Output scores',
                data: results.map(item => item[1]), // Extract scores dynamically
                backgroundColor: [
                    'rgba(26,74,4,0.8)',
                    'rgba(117,0,20,0.8)',
                    'rgba(121,87,3,0.8)',
                    'rgba(6,33,108,0.8)',
                    'rgba(63,3,85,0.8)',
                ],
                borderColor: [
                    'rgba(26,74,4)',
                    'rgba(117,0,20)',
                    'rgba(121,87,3)',
                    'rgba(6,33,108)',
                    'rgba(63,3,85)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
