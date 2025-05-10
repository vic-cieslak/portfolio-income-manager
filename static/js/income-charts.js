// Income trend chart initialization
function initIncomeChart() {
    try {
        const canvas = document.getElementById('incomeChart');
        if (!canvas) {
            console.warn('Chart canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        
        // Use the global variables directly
        console.log("Chart Labels:", window.chartLabels);
        console.log("Chart Values:", window.chartValues);
        
        // Check if data exists
        if (!window.chartLabels || !window.chartValues || 
            window.chartLabels.length === 0 || window.chartValues.length === 0) {
            console.warn('No chart data available');
            return;
        }
        
        // Use the global variables for chart data
        const chartLabels = window.chartLabels;
        const chartData = window.chartValues;
        
        const gradientFill = ctx.createLinearGradient(0, 0, 0, 200);
        gradientFill.addColorStop(0, 'rgba(0, 255, 157, 0.7)');
        gradientFill.addColorStop(1, 'rgba(0, 255, 157, 0.1)');
    
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Monthly Income',
                    data: chartData,
                    borderColor: '#00ff9d',
                    borderWidth: 2,
                    pointBackgroundColor: '#00ff9d',
                    pointBorderColor: '#00ff9d',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#00ff9d',
                    // pointRadius: 4, // Not applicable for bar charts
                    // pointHoverRadius: 6, // Not applicable for bar charts
                    // fill: true, // Fill is generally handled differently or not needed for bar charts
                    backgroundColor: gradientFill, // For bar charts, this often sets the bar color
                    // tension: 0.3 // Not applicable for bar charts
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 20, 40, 0.8)',
                        titleColor: '#00ff9d',
                        bodyColor: '#e0e0ff',
                        borderColor: '#00ff9d',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(0, 255, 157, 0.1)',
                            borderColor: 'rgba(0, 255, 157, 0.2)'
                        },
                        ticks: {
                            color: '#8f9fbc'
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(0, 255, 157, 0.1)',
                            borderColor: 'rgba(0, 255, 157, 0.2)'
                        },
                        ticks: {
                            color: '#8f9fbc',
                            callback: function(value) {
                                return 'PLN ' + value;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating chart:', error);
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('incomeChart')) {
        initIncomeChart();
    }
});
