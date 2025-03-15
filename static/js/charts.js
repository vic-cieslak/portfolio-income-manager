// @ts-nocheck

/** @type {string[]} */
let portfolioLabels = [];
/** @type {number[]} */
let portfolioData = [];
/** @type {string[]} */
let cryptoNames = [];
/** @type {number[]} */
let cryptoValues = [];
/** @type {string[]} */
let colors = [];

/**
 * Function to safely initialize charts
 */
function initCharts() {
    // Portfolio Chart
    if (document.getElementById('portfolioChart')) {
        // Check if chart instance already exists and destroy it
        const chartInstance = Chart.getChart('portfolioChart');
        if (chartInstance) {
            chartInstance.destroy();
        }

        var portfolioCtx = document.getElementById('portfolioChart').getContext('2d');
        var portfolioChart = new Chart(portfolioCtx, {
            type: 'doughnut',
            data: {
                labels: portfolioLabels,
                datasets: [{
                    data: portfolioData,
                    backgroundColor: [
                        'rgba(0, 255, 157, 0.8)',  // Crypto - Cyberpunk green
                        'rgba(0, 184, 255, 0.8)', // Bank - Cyberpunk blue
                    ],
                    borderColor: [
                        'rgba(0, 255, 157, 1)',
                        'rgba(0, 184, 255, 1)',
                    ],
                    borderWidth: 2,
                    hoverBackgroundColor: [
                        'rgba(0, 255, 157, 1)',
                        'rgba(0, 184, 255, 1)',
                    ],
                    hoverBorderColor: [
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)',
                    ],
                    hoverBorderWidth: 4,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                layout: {
                    padding: 20
                },
                plugins: {
                    legend: {
                        display: false, // Hide default legend
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 23, 0.9)',
                        titleFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 14
                        },
                        padding: 15,
                        cornerRadius: 0,
                        displayColors: false,
                        callbacks: {
                            title: function(tooltipItems) {
                                return tooltipItems[0].label.toUpperCase();
                            },
                            label: function(context) {
                                var value = context.raw || 0;
                                var total = context.dataset.data.reduce(function(acc, val) { return acc + val; }, 0);
                                var percentage = Math.round((value / total) * 100);
                                return `PLN ${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 2000,
                    easing: 'easeOutQuart'
                },
                onHover: (event, chartElement) => {
                    event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default';
                },
                onClick: (event, chartElement) => {
                    if (chartElement.length > 0) {
                        const index = chartElement[0].index;
                        const label = portfolioLabels[index];
                        const value = portfolioData[index];
                        showDetailModal(label, value);
                    }
                }
            }
        });

        // Custom legend
        createCustomLegend(portfolioChart, 'portfolioChartLegend');
    }
}

// Function to create a custom legend
function createCustomLegend(chart, legendId) {
    const legendContainer = document.getElementById(legendId);
    legendContainer.innerHTML = '';

    const ul = document.createElement('ul');
    ul.style.display = 'flex';
    ul.style.flexWrap = 'wrap';
    ul.style.justifyContent = 'center';
    ul.style.padding = '0';
    ul.style.margin = '20px 0 0';

    chart.data.labels.forEach((label, index) => {
        const li = document.createElement('li');
        li.style.display = 'flex';
        li.style.alignItems = 'center';
        li.style.margin = '0 15px 10px';
        li.style.cursor = 'pointer';

        const boxSpan = document.createElement('span');
        boxSpan.style.width = '20px';
        boxSpan.style.height = '20px';
        boxSpan.style.backgroundColor = chart.data.datasets[0].backgroundColor[index];
        boxSpan.style.borderRadius = '3px';
        boxSpan.style.marginRight = '10px';
        boxSpan.style.boxShadow = '0 0 5px ' + chart.data.datasets[0].backgroundColor[index];

        const textContainer = document.createElement('div');
        textContainer.style.display = 'flex';
        textContainer.style.flexDirection = 'column';

        const labelSpan = document.createElement('span');
        labelSpan.textContent = label;
        labelSpan.style.color = '#e0e0ff';
        labelSpan.style.fontFamily = 'Share Tech Mono, monospace';
        labelSpan.style.fontSize = '14px';

        const valueSpan = document.createElement('span');
        const value = chart.data.datasets[0].data[index];
        const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
        const percentage = ((value / total) * 100).toFixed(1);
        valueSpan.textContent = `PLN ${value.toLocaleString()} (${percentage}%)`;
        valueSpan.style.color = '#8f9fbc';
        valueSpan.style.fontFamily = 'Share Tech Mono, monospace';
        valueSpan.style.fontSize = '12px';

        textContainer.appendChild(labelSpan);
        textContainer.appendChild(valueSpan);

        li.appendChild(boxSpan);
        li.appendChild(textContainer);

        li.addEventListener('mouseover', () => {
            boxSpan.style.boxShadow = '0 0 15px ' + chart.data.datasets[0].backgroundColor[index];
        });

        li.addEventListener('mouseout', () => {
            boxSpan.style.boxShadow = '0 0 5px ' + chart.data.datasets[0].backgroundColor[index];
        });

        li.addEventListener('click', () => {
            showDetailModal(label, value);
        });

        ul.appendChild(li);
    });

    legendContainer.appendChild(ul);
}

// Function to show detail modal
function showDetailModal(label, value) {
    const modalContent = `
        <h3>${label} Details</h3>
        <p>Value: PLN ${value.toLocaleString()}</p>
        <p>Additional details can be added here.</p>
    `;
    
    // You can implement a modal display logic here
    // For now, we'll just log to console
    console.log('Showing modal for:', modalContent);
    // In a real implementation, you would create and show a modal with this content
}

// Crypto Chart
function initCryptoChart() {
    console.log('initCryptoChart called');
    console.log('cryptoNames:', window.cryptoNames);
    console.log('cryptoValues:', window.cryptoValues);
    console.log('colors:', window.colors);
    
    // Check if we have data to display
    if (!window.cryptoNames || !window.cryptoValues || window.cryptoNames.length === 0 || window.cryptoValues.length === 0) {
        console.error('No crypto data available for chart');
        return;
    }
    
    const cryptoChartElement = document.getElementById('cryptoChart');
    if (!cryptoChartElement) {
        console.error('cryptoChart element not found in DOM');
        return;
    }
    console.log('cryptoChart element found');
    
    const chartInstance = Chart.getChart('cryptoChart');
    if (chartInstance) {
        console.log('Destroying existing chart instance');
        chartInstance.destroy();
    }

    try {
        const ctx = cryptoChartElement.getContext('2d');
        console.log('Got 2d context');
        
        // Create enhanced colors with better visibility
        const enhancedColors = window.colors.slice(0, window.cryptoNames.length).map(color => lightenColor(color));
        
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: window.cryptoNames,
                datasets: [{
                    data: window.cryptoValues,
                    backgroundColor: enhancedColors,
                    borderColor: '#000',
                    borderWidth: 2,
                    hoverOffset: 15,
                    hoverBorderWidth: 3,
                    hoverBorderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e0e0ff',
                            font: {
                                family: 'Share Tech Mono, monospace',
                                size: 14
                            },
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 23, 0.9)',
                        titleFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 14
                        },
                        padding: 15,
                        cornerRadius: 0,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: PLN ${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
        console.log('Crypto chart created successfully');
    } catch (error) {
        console.error('Error creating crypto chart:', error);
        console.error('Error details:', error.message);
        console.error('Error stack:', error.stack);
    }
}

function lightenColor(color) {
    const rgb = hexToRgb(color);
    const lightenedRgb = rgb.map(val => Math.min(255, val + 50));
    return rgbToHex(lightenedRgb);
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : null;
}

function rgbToHex(rgb) {
    return "#" + rgb.map(val => val.toString(16).padStart(2, '0')).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    initCryptoChart();
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initCharts, initCryptoChart };
}
