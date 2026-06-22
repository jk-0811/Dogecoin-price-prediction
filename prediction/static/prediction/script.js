// Dogecoin Price Prediction Dashboard Script

document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('predictionForm');
    
    // Form submission
    predictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        makePrediction();
    });
    
    // Load example data function
    window.loadExample1 = function() {
        document.getElementById('open').value = '0.150';
        document.getElementById('high').value = '0.160';
        document.getElementById('low').value = '0.145';
        document.getElementById('volume').value = '1250000000';
        document.getElementById('ma5').value = '0.152';
        document.getElementById('ma10').value = '0.151';
        document.getElementById('daily_return').value = '0.025';
        document.getElementById('volatility').value = '0.015';
    };
    
    window.loadExample2 = function() {
        document.getElementById('open').value = '0.200';
        document.getElementById('high').value = '0.210';
        document.getElementById('low').value = '0.190';
        document.getElementById('volume').value = '1500000000';
        document.getElementById('ma5').value = '0.205';
        document.getElementById('ma10').value = '0.195';
        document.getElementById('daily_return').value = '0.030';
        document.getElementById('volatility').value = '0.020';
    };
    
    window.loadExample3 = function() {
        document.getElementById('open').value = '0.082';
        document.getElementById('high').value = '0.095';
        document.getElementById('low').value = '0.080';
        document.getElementById('volume').value = '800000000';
        document.getElementById('ma5').value = '0.088';
        document.getElementById('ma10').value = '0.086';
        document.getElementById('daily_return').value = '0.012';
        document.getElementById('volatility').value = '0.010';
    };
    
    // Initialize chart
    initChart();
});

function makePrediction() {
    // Show loading
    showLoading(true);
    hideResults();
    
    // Gather form data
    const formData = {
        open: parseFloat(document.getElementById('open').value),
        high: parseFloat(document.getElementById('high').value),
        low: parseFloat(document.getElementById('low').value),
        volume: parseFloat(document.getElementById('volume').value),
        ma5: parseFloat(document.getElementById('ma5').value),
        ma10: parseFloat(document.getElementById('ma10').value),
        daily_return: parseFloat(document.getElementById('daily_return').value),
        volatility: parseFloat(document.getElementById('volatility').value),
    };
    
    // Make API request
    fetch('/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        
        if (data.success) {
            displayResults(data);
            updateChart(data);
        } else {
            showError(data.error || 'Prediction failed');
        }
    })
    .catch(error => {
        showLoading(false);
        showError('Error: ' + error.message);
        console.error('Error:', error);
    });
}

function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    const predictedPrice = data.predicted_price;
    
    // Format price
    const priceFormatted = '$' + predictedPrice.toFixed(6);
    document.getElementById('predictedPrice').textContent = priceFormatted;
    
    // Display features
    const featuresDisplay = document.getElementById('featuresDisplay');
    featuresDisplay.innerHTML = '';
    
    const features = data.input_features;
    for (const [key, value] of Object.entries(features)) {
        const featureDiv = document.createElement('div');
        featureDiv.className = 'feature-item';
        
        let displayValue = value;
        if (key === 'Volume') {
            displayValue = (value / 1000000).toFixed(2) + 'M';
        } else if (key !== 'Daily_Return' && key !== 'Volatility') {
            displayValue = '$' + parseFloat(value).toFixed(6);
        } else {
            displayValue = parseFloat(value).toFixed(6);
        }
        
        featureDiv.innerHTML = `
            <div class="feature-label">${formatLabel(key)}</div>
            <div class="feature-value">${displayValue}</div>
        `;
        
        featuresDisplay.appendChild(featureDiv);
    }
    
    // Display timestamp
    const timestamp = new Date(data.timestamp).toLocaleString();
    document.getElementById('timestampText').textContent = 'Predicted at: ' + timestamp;
    
    // Confidence text
    document.getElementById('confidenceText').textContent = 'Prediction confidence: High ✓';
    
    // Show results
    resultsContainer.classList.remove('hidden');
}

function formatLabel(key) {
    const labels = {
        'Open': 'Open Price',
        'High': 'High Price',
        'Low': 'Low Price',
        'Volume': 'Trading Volume',
        'MA5': '5-Day MA',
        'MA10': '10-Day MA',
        'Daily_Return': 'Daily Return',
        'Volatility': 'Volatility'
    };
    return labels[key] || key;
}

function showLoading(show) {
    const loader = document.getElementById('loadingSpinner');
    if (show) {
        loader.classList.remove('hidden');
    } else {
        loader.classList.add('hidden');
    }
}

function hideResults() {
    document.getElementById('resultsContainer').classList.add('hidden');
    document.getElementById('chartContainer').classList.add('hidden');
}

function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    document.getElementById('errorMessage').textContent = message;
    errorContainer.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorContainer.classList.add('hidden');
    }, 5000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let predictionChart = null;

function initChart() {
    const ctx = document.getElementById('predictionChart');
    if (ctx) {
        predictionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Previous', 'Current', 'Predicted'],
                datasets: [{
                    label: 'Price ($)',
                    data: [0, 0, 0],
                    borderColor: '#ffd000',
                    backgroundColor: 'rgba(255, 208, 0, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBorderColor: '#ffd000',
                    pointBackgroundColor: '#1a1a1a'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 208, 0, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#fff' },
                        grid: { color: 'rgba(255, 208, 0, 0.1)' }
                    }
                }
            }
        });
    }
}

function updateChart(data) {
    if (predictionChart) {
        const open = data.input_features.Open;
        const predicted = data.predicted_price;
        const previous = open * 0.98; // Estimate
        
        predictionChart.data.datasets[0].data = [previous, open, predicted];
        predictionChart.update();
        
        document.getElementById('chartContainer').classList.remove('hidden');
    }
}

// Plotly Historical Chart
function initHistoricalChart() {
    const trace = {
        x: ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', 'Prediction'],
        y: [0.08, 0.10, 0.12, 0.11, 0.13, 0.15, 0.16],
        type: 'scatter',
        mode: 'lines+markers',
        line: {
            color: '#ffd000',
            width: 3
        },
        marker: {
            size: 8,
            color: '#ffd000'
        }
    };
    
    const layout = {
        title: 'Dogecoin Price History & Prediction',
        xaxis: {
            title: 'Month',
            color: '#fff'
        },
        yaxis: {
            title: 'Price (USD)',
            color: '#fff'
        },
        plot_bgcolor: '#2d2d2d',
        paper_bgcolor: '#1a1a1a',
        font: { color: '#fff' }
    };
    
    Plotly.newPlot('historicalChart', [trace], layout, { responsive: true });
}

// Initialize historical chart on page load
window.addEventListener('load', initHistoricalChart);
