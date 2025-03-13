// Function to safely initialize charts
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
                        'rgba(255, 234, 167, 0.8)',  // Lighter Crypto - yellow/gold
                        'rgba(153, 204, 255, 0.8)', // Lighter Bank - blue
                    ],
                    borderColor: [
                        'rgba(255, 171, 0, 1)',
                        'rgba(33, 150, 243, 1)',
                    ],
                    borderWidth: 2,
                    hoverBackgroundColor: [
                        'rgba(255, 234, 167, 0.9)',
                        'rgba(153, 204, 255, 0.9)',
                    ],
                    hoverBorderWidth: 3,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Inter, sans-serif',
                                size: 13,
                                weight: 500
                            },
                            color: '#b0b0b0',
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(20, 20, 20, 0.9)',
                        titleFont: {
                            family: 'Inter, sans-serif',
                            size: 13
                        },
                        bodyFont: {
                            family: 'Inter, sans-serif',
                            size: 14,
                            weight: 500
                        },
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                var label = context.label || '';
                                var value = context.raw || 0;
                                var total = context.dataset.data.reduce(function(acc, val) { return acc + val; }, 0);
                                var percentage = Math.round((value / total) * 100);
                                return label + ': PLN ' + value.toLocaleString() + ' (' + percentage + '%)';
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 2000,
                    easing: 'easeOutCirc'
                }
            }
        });
    }

    // Crypto Chart
    if (document.getElementById('cryptoChart')) {
        // Check if chart instance already exists and destroy it
        const chartInstance = Chart.getChart('cryptoChart');
        if (chartInstance) {
            chartInstance.destroy();
        }

        const ctx = document.getElementById('cryptoChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: cryptoNames,
                datasets: [{
                    data: cryptoValues,
                    backgroundColor: colors.slice(0, cryptoNames.length).map(color => lightenColor(color)), //Apply lightening function
                    borderColor: '#000',
                    borderWidth: 2
                }]
            },
            options: {
                plugins: {
                    legend: {
                        labels: {
                            color: '#0ff',
                            font: {
                                family: 'monospace',
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce(function(acc, val) { return acc + val; }, 0);
                                const percentage = Math.round((value / total) * 100);
                                return label + ': PLN ' + value.toLocaleString() + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    }
}


function lightenColor(color) {
    // Simple lightening function - adjust as needed for your color scheme
    const rgb = hexToRgb(color);
    const lightenedRgb = rgb.map(val => Math.min(255, val + 50)); //Increase each RGB value by 50, clamping at 255
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

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Call the function to initialize charts
    initCharts();
});