

document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing 5-hour forecast chart...');
    

    const forecastSection = document.querySelector('.forecast-section');
    if (!forecastSection) {
        console.log('Forecast section not found - not initializing chart');
        return;
    }


    const weatherData = extractForecastData();
    console.log('Forecast data extracted:', weatherData);


    initializeForecastChart(weatherData);
});

function extractForecastData() {
    // Extract time data
    const timeElements = document.querySelectorAll('.time-data');
    const times = Array.from(timeElements).map(el => el.textContent.trim());

    // Extract temperature data
    const tempElements = document.querySelectorAll('.temp-data');
    const temperatures = Array.from(tempElements).map(el => parseFloat(el.textContent.trim()) || 0);

    // Extract humidity data
    const humidityElements = document.querySelectorAll('.humidity-data');
    const humidity = Array.from(humidityElements).map(el => parseFloat(el.textContent.trim()) || 0);

    // Use fallback data if extraction failed
    if (times.length === 0 || temperatures.length === 0 || humidity.length === 0) {
        console.warn('Failed to extract forecast data, using fallback data');
        return getFallbackData();
    }

    return { times, temperatures, humidity };
}

function getFallbackData() {
    return {
        times: ['14:00', '15:00', '16:00', '17:00', '18:00'],
        temperatures: [22, 24, 23, 21, 19],
        humidity: [65, 62, 68, 70, 72]
    };
}


function initializeForecastChart(data) {
    // Create temperature chart
    createTemperatureChart(data);
    
    // Create humidity bars
    createHumidityBars(data);
    
    // Update statistics
    updateStatistics(data);
}

function createTemperatureChart(data) {
    const dataPointsGroup = document.getElementById('dataPoints');
    const tempPath = document.getElementById('tempPath');
    
    if (!dataPointsGroup || !tempPath) {
        console.error('Temperature chart elements not found');
        return;
    }

    // Clear existing data points
    dataPointsGroup.innerHTML = '';
    
    const { times, temperatures } = data;
    
    // Calculate temperature range for scaling
    const maxTemp = Math.max(...temperatures);
    const minTemp = Math.min(...temperatures);
    const tempRange = maxTemp - minTemp || 1;
    
    // Generate SVG path points
    const pathPoints = [];
    
    temperatures.forEach((temp, index) => {
        // Calculate position
        const x = 40 + (index * 520) / (temperatures.length - 1);
        const y = 60 - ((temp - minTemp) / tempRange) * 40;
        pathPoints.push(`${x},${y}`);
        
        // Create temperature point circle
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', x);
        circle.setAttribute('cy', y);
        circle.setAttribute('r', '4');
        circle.setAttribute('fill', 'white');
        circle.setAttribute('stroke', '#3B82F6');
        circle.setAttribute('stroke-width', '2');
        circle.style.opacity = '0';
        circle.style.animation = `fadeIn 0.3s ease-out ${1.2 + index * 0.1}s forwards`;
        dataPointsGroup.appendChild(circle);
        
        // Create temperature label
        const tempLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        tempLabel.setAttribute('x', x);
        tempLabel.setAttribute('y', y - 12);
        tempLabel.setAttribute('text-anchor', 'middle');
        tempLabel.setAttribute('fill', 'white');
        tempLabel.setAttribute('font-size', '11');
        tempLabel.setAttribute('font-weight', '600');
        tempLabel.textContent = `${Math.round(temp)}°`;
        tempLabel.style.opacity = '0';
        tempLabel.style.animation = `fadeIn 0.3s ease-out ${1.3 + index * 0.1}s forwards`;
        dataPointsGroup.appendChild(tempLabel);
        
        // Create time label
        const timeLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        timeLabel.setAttribute('x', x);
        timeLabel.setAttribute('y', 110);
        timeLabel.setAttribute('text-anchor', 'middle');
        timeLabel.setAttribute('fill', 'white');
        timeLabel.setAttribute('font-size', '10');
        timeLabel.setAttribute('opacity', '0.7');
        timeLabel.textContent = times[index];
        timeLabel.style.opacity = '0';
        timeLabel.style.animation = `fadeIn 0.3s ease-out ${1.4 + index * 0.1}s forwards`;
        dataPointsGroup.appendChild(timeLabel);
    });
    
    // Update temperature path
    const pathData = 'M ' + pathPoints.join(' L ');
    tempPath.setAttribute('d', pathData);
    
    // Animate the path drawing
    tempPath.style.strokeDasharray = '1000';
    tempPath.style.strokeDashoffset = '1000';
    tempPath.style.animation = 'none';
    tempPath.offsetHeight; // Force reflow
    tempPath.style.animation = 'drawPath 1.5s ease-in-out 1s forwards';
}

function createHumidityBars(data) {
    const humidityGrid = document.getElementById('humidityGrid');
    
    if (!humidityGrid) {
        console.error('Humidity grid not found');
        return;
    }
    
    // Clear existing humidity items
    humidityGrid.innerHTML = '';
    
    data.humidity.forEach((humidityValue, index) => {
        // Create humidity item container
        const humidityItem = document.createElement('div');
        humidityItem.className = 'humidity-item';
        humidityItem.style.opacity = '0';
        humidityItem.style.animation = `fadeIn 0.4s ease-out ${1.5 + index * 0.1}s forwards`;
        
        // Create humidity value display
        const humidityValueDiv = document.createElement('div');
        humidityValueDiv.className = 'humidity-value';
        humidityValueDiv.textContent = `${Math.round(humidityValue)}%`;
        
        // Create humidity bar container
        const humidityBar = document.createElement('div');
        humidityBar.className = 'humidity-bar';
        
        // Create humidity fill bar
        const humidityFill = document.createElement('div');
        humidityFill.className = 'humidity-fill';
        humidityFill.style.width = '0%';
        
        // Assemble humidity elements
        humidityBar.appendChild(humidityFill);
        humidityItem.appendChild(humidityValueDiv);
        humidityItem.appendChild(humidityBar);
        humidityGrid.appendChild(humidityItem);
        
        // Animate humidity bar fill
        setTimeout(() => {
            humidityFill.style.width = `${Math.min(100, Math.max(0, humidityValue))}%`;
        }, 1600 + index * 100);
    });
}


function updateStatistics(data) {
    const tempRangeStat = document.getElementById('tempRangeStat');
    const avgHumidityStat = document.getElementById('avgHumidityStat');
    
    if (!tempRangeStat || !avgHumidityStat) {
        console.error('Statistics elements not found');
        return;
    }
    
    // Calculate statistics
    const maxTemp = Math.max(...data.temperatures);
    const minTemp = Math.min(...data.temperatures);
    const avgHumidity = Math.round(data.humidity.reduce((sum, h) => sum + h, 0) / data.humidity.length);
    
    // Update temperature range
    tempRangeStat.textContent = `${Math.round(maxTemp)}° - ${Math.round(minTemp)}°`;
    
    // Update average humidity
    avgHumidityStat.textContent = `${avgHumidity}%`;
}

function addChartAnimations() {
    // Check if animations are already added
    if (document.getElementById('chart-animations')) {
        return;
    }
    
    // Create style element
    const style = document.createElement('style');
    style.id = 'chart-animations';
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes drawPath {
            from { stroke-dashoffset: 1000; }
            to { stroke-dashoffset: 0; }
        }
        
        .humidity-fill {
            transition: width 0.6s ease-out;
        }
    `;
    
    // Add style to document
    document.head.appendChild(style);
}

// Initialize animations
addChartAnimations();

















