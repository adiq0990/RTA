// URL
const url = 'http://127.0.0.1:5000';

// ZMIENNE PRZECHOWUJĄCE WYKRESY
let chart_provinces;
let age_histogram;

// FUNKCJA DO NISZCZENIA WYKRESOW
function destroyChart(chart) {
  if(chart) {
    chart.destroy();
  }
}

setInterval(() => {
  fetchData(url, '/chart_provinces');
  fetchData(url, '/age_histogram');
}, 5000);


async function fetchData(url, endpoint) {
    const response = await fetch(`${url}${endpoint}`);
    const data = await response.json();
    console.log('Received data:', data);
    

    if (endpoint === '/chart_provinces') {
      destroyChart(chart_provinces);
      drawProvinceChart(data);
    }

    if (endpoint === '/age_histogram') {
      destroyChart(age_histogram);
      drawAgeHistogram(data);
    }
}

function drawAgeHistogram(data) {
    const ctx = document.getElementById('age-histogram').getContext('2d');
    
    age_histogram = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.age_groups,
            datasets: [{
                data: data.count_sum,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


function drawProvinceChart(data) {
    const ctx = document.getElementById('province-chart').getContext('2d');
    
    chart_provinces = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.provinces,
            datasets: [{
                label: 'Zachorowania w województwach',
                data: data.count_sum,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
