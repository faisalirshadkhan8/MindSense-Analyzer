// Ensure form submission works
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sentimentForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const textarea = this.querySelector('textarea');
            if (!textarea.value.trim()) {
                e.preventDefault();
                textarea.classList.add('is-invalid');
                alert('Please enter some text to analyze.');
            }
        });
    }

    // Apply animation delays from data attributes
    document.querySelectorAll('.suggestion-item[data-delay]').forEach(item => {
        const delay = item.getAttribute('data-delay');
        if (delay) {
            item.style.animationDelay = `${delay}s`;
        }
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initialize charts if data exists
    if (typeof dailyLabels !== 'undefined' && typeof dailyData !== 'undefined') {
        initializeCharts();
    }
});

// Function to initialize all charts
function initializeCharts() {
    const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDarkMode ? '#ffffff' : '#333333';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    
    // Daily Sentiment Trend
    const dailySentimentCanvas = document.getElementById('dailySentimentChart');
    let dailyChart;
    if (dailySentimentCanvas) {
        const dailySentimentCtx = dailySentimentCanvas.getContext('2d');
        dailyChart = new Chart(dailySentimentCtx, {
            type: 'line',
            data: {
                labels: dailyLabels,
                datasets: [{
                    label: 'Average Sentiment',
                    data: dailyData,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Daily Sentiment Trend',
                        color: textColor
                    },
                    legend: {
                        labels: {
                            color: textColor
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    },
                    x: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    } else {
        console.warn("Canvas element with ID 'dailySentimentChart' not found.");
    }

    // Emotion Distribution
    const emotionCanvas = document.getElementById('emotionChart');
    let emotionChart;
    if (emotionCanvas) {
        const emotionCtx = emotionCanvas.getContext('2d');
        emotionChart = new Chart(emotionCtx, {
            type: 'doughnut',
            data: {
                labels: emotionLabels,
                datasets: [{
                    data: emotionData,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                        '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Emotion Distribution',
                        color: textColor
                    },
                    legend: {
                        position: 'right',
                        labels: {
                            color: textColor
                        }
                    }
                }
            }
        });
    } else {
        console.warn("Canvas element with ID 'emotionChart' not found.");
    }

    // Sentiment Distribution
    const sentimentCanvas = document.getElementById('sentimentChart');
    let sentimentChart;
    if (sentimentCanvas) {
        const sentimentCtx = sentimentCanvas.getContext('2d');
        sentimentChart = new Chart(sentimentCtx, {
            type: 'bar',
            data: {
                labels: sentimentLabels,
                datasets: [{
                    label: 'Count',
                    data: sentimentData,
                    backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Sentiment Distribution',
                        color: textColor
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    },
                    x: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    } else {
        console.warn("Canvas element with ID 'sentimentChart' not found.");
    }

    // Update charts on theme change
    window.addEventListener('themeChanged', function (e) {
        const isDark = e.detail === 'dark';
        const newTextColor = isDark ? '#ffffff' : '#333333';
        const newGridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

        const updateChart = function(chart) {
            if (chart && chart.options) {
                if (chart.options.plugins.title) {
                    chart.options.plugins.title.color = newTextColor;
                }
                if (chart.options.plugins.legend && chart.options.plugins.legend.labels) {
                    chart.options.plugins.legend.labels.color = newTextColor;
                }
                if (chart.options.scales) {
                    Object.values(chart.options.scales).forEach(function(scale) {
                        if (scale.ticks) scale.ticks.color = newTextColor;
                        if (scale.grid) scale.grid.color = newGridColor;
                    });
                }
                chart.update();
            }
        };

        // Create an array of charts that exist
        const chartsToUpdate = [];
        if (dailyChart) chartsToUpdate.push(dailyChart);
        if (emotionChart) chartsToUpdate.push(emotionChart);
        if (sentimentChart) chartsToUpdate.push(sentimentChart);
        
        chartsToUpdate.forEach(updateChart);
    });
}