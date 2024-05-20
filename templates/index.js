// URL
const url = 'http://127.0.0.1:5000';

// ZMIENNE PRZECHOWUJĄCE WYKRESY
let chart_provinces;
let age_histogram;
let number_cases;

// FUNKCJA DO NISZCZENIA WYKRESOW
function destroyChart(chart) {
  if(chart) {
    chart.destroy();
  }
}

setInterval(() => {
  fetchData(url, '/chart_provinces');
  fetchData(url, '/age_histogram');
  fetchData(url, '/number_cases')
  fetchData(url, '/data_summary')
}, 5000);

let currentScrollPosition = 0;

async function fetchData(url, endpoint) {

    currentScrollPosition = window.pageYOffset;

    const response = await fetch(`${url}${endpoint}`);
    const data = await response.json();
    console.log('Received data:', data);

    window.scrollTo(0, currentScrollPosition);
    

    if (endpoint === '/chart_provinces') {
        destroyChart(chart_provinces);
        drawProvinceChart(data);
    }

    if (endpoint === '/age_histogram') {
        destroyChart(age_histogram);
        drawAgeHistogram(data);
    }

    if (endpoint === '/number_cases') {
        destroyChart(number_cases);
        drawNumberCases(data);
    }

    if (endpoint === '/data_summary') {
        document.getElementById('total_cases').innerHTML = data.cases;
        document.getElementById('active_cases').innerHTML = data.active;
        document.getElementById('total_deaths').innerHTML = data.deaths;
        document.getElementById('total_recovered').innerHTML = data.recovered;
    }


}

function drawNumberCases(data) {
    const ctx = document.getElementById('pie_cases').getContext('2d');

    number_cases = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.sizes,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            radius: '70%',
        }
    });
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
