
// Dashboard Charts
document.addEventListener('DOMContentLoaded', function() {
  // Portfolio allocation chart
  const portfolioCtx = document.getElementById('portfolioChart');
  
  if (portfolioCtx) {
    // Get data from the page
    const portfolioData = JSON.parse(portfolioCtx.dataset.values || '[]');
    const portfolioLabels = JSON.parse(portfolioCtx.dataset.labels || '[]');
    
    // Calculate total for center text
    const totalValue = portfolioData.reduce((a, b) => a + b, 0);
    
    // Create chart with proper config
    const portfolioChart = new Chart(portfolioCtx, {
      type: 'doughnut',
      data: {
        labels: portfolioLabels,
        datasets: [{
          data: portfolioData,
          backgroundColor: ['#ffc107', '#0d6efd'],
          borderColor: ['rgba(255, 193, 7, 0.8)', 'rgba(13, 110, 253, 0.8)'],
          borderWidth: 1,
          hoverOffset: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        cutout: '70%',
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            titleFont: {
              size: 14
            },
            bodyFont: {
              size: 13
            },
            callbacks: {
              label: function(context) {
                const value = context.parsed;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value * 100) / total);
                return `${context.label}: ${percentage}% (${value} PLN)`;
              }
            }
          }
        },
        animation: {
          animateScale: true,
          animateRotate: true
        }
      }
    });
  }

  // Income monthly chart
  const incomeCtx = document.getElementById('incomeChart');
  
  if (incomeCtx) {
    const incomeData = JSON.parse(incomeCtx.dataset.values || '[]');
    const incomeLabels = JSON.parse(incomeCtx.dataset.labels || '[]');
    
    new Chart(incomeCtx, {
      type: 'bar',
      data: {
        labels: incomeLabels,
        datasets: [{
          label: 'Monthly Income',
          data: incomeData,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)'
            }
          },
          x: {
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.7)'
            }
          }
        }
      },
      plugins: [{
        id: 'centerText',
        beforeDraw: function(chart) {
          const width = chart.width;
          const height = chart.height;
          const ctx = chart.ctx;
          
          ctx.restore();
          
          // Font size based on canvas size
          const fontSize = (height / 180).toFixed(2);
          ctx.font = `bold ${fontSize}em 'Inter', sans-serif`;
          ctx.textBaseline = 'middle';
          ctx.textAlign = 'center';
          
          // Value text
          const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
          const text = `PLN ${total.toLocaleString('pl-PL', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
          ctx.fillStyle = '#f5f5f5';
          ctx.fillText(text, width/2, height/2 - height/25);
          
          // Label text
          ctx.font = `${fontSize * 0.5}em 'Inter', sans-serif`;
          ctx.fillStyle = '#707070';
          ctx.fillText('TOTAL ASSETS', width/2, height/2 + height/15);
          
          ctx.save();
        }
      }]
    });
  }
});
