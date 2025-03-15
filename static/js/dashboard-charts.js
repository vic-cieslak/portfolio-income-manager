function initCharts() {
    console.log('Initializing charts...');
    console.log('Chart data:', window.chartData);
    if (!window.chartData) {
        console.error('Chart data is not available');
        return;
    }
    try {
        initPortfolioChart();
        initIncomeExpenseChart();
    } catch (error) {
        console.error('Error initializing charts:', error);
        console.error('Error details:', error.message);
        console.error('Error stack:', error.stack);
        alert('There was an error initializing the charts. Please check the console for more information.');
    }
}

function initPortfolioChart() {
    console.log('Initializing portfolio chart...');
    const ctx = document.getElementById('portfolioChart');
    if (!ctx) {
        console.error('Portfolio chart canvas not found');
        return;
    }
    if (!window.chartData.portfolioLabels || !window.chartData.portfolioData) {
        console.error('Portfolio chart data is missing');
        return;
    }
    const portfolioChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: window.chartData.portfolioLabels,
            datasets: [{
                data: window.chartData.portfolioData,
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
            plugins: {
                legend: {
                    display: false,
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
                        label: function(context) {
                            const value = context.raw;
                            const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
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
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    const label = window.chartData.portfolioLabels[index];
                    const value = window.chartData.portfolioData[index];
                    showDetailModal(label, value);
                }
            }
        }
    });

    createCustomLegend(portfolioChart, 'portfolioChartLegend');
}

function initIncomeExpenseChart() {
    console.log('Initializing income/expense chart...');
    const ctx = document.getElementById('incomeExpenseChart');
    if (!ctx) {
        console.error('Income/Expense chart canvas not found');
        return;
    }
    if (!window.chartData.monthLabels || !window.chartData.incomeData || !window.chartData.expenseData) {
        console.error('Income/Expense chart data is missing');
        return;
    }
    try {
        new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: window.chartData.monthLabels,
                datasets: [
                    {
                        label: 'Income',
                        data: window.chartData.incomeData,
                        backgroundColor: 'rgba(0, 255, 157, 0.7)',
                        borderColor: 'rgba(0, 255, 157, 1)',
                        borderWidth: 0,
                        borderRadius: 6,
                        hoverBackgroundColor: 'rgba(0, 255, 157, 0.9)',
                        barPercentage: 0.7,
                        categoryPercentage: 0.8
                    },
                    {
                        label: 'Expenses',
                        data: window.chartData.expenseData,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 0,
                        borderRadius: 6,
                        hoverBackgroundColor: 'rgba(255, 99, 132, 0.9)',
                        barPercentage: 0.7,
                        categoryPercentage: 0.8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                family: 'Share Tech Mono, monospace',
                                size: 12
                            },
                            color: '#e0e0ff'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(10, 14, 23, 0.9)',
                        titleFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 13
                        },
                        bodyFont: {
                            family: 'Share Tech Mono, monospace',
                            size: 14
                        },
                        padding: 12,
                        cornerRadius: 0,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': PLN ' + context.raw.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            font: {
                                family: 'Share Tech Mono, monospace',
                                size: 12
                            },
                            color: '#00ff9d'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 255, 157, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            font: {
                                family: 'Share Tech Mono, monospace',
                                size: 12
                            },
                            color: '#00ff9d',
                            callback: function(value) {
                                return 'PLN ' + value.toLocaleString();
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    } catch (error) {
        console.error('Error creating income/expense chart:', error);
    }
}

function createCustomLegend(chartId, legendId) {
    const chart = Chart.getChart(chartId);
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

function showDetailModal(label, value) {
    const modalContent = `
        <h3>${label} Details</h3>
        <p>Value: PLN ${value.toLocaleString()}</p>
        <p>Additional details can be added here.</p>
    `;
    
    console.log('Showing modal for:', modalContent);
    // Implement modal display logic here
}
