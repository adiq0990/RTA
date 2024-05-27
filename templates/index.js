// URL
const url = 'http://127.0.0.1:5000';

// ZMIENNE PRZECHOWUJĄCE WYKRESY
let provinces_histograms = {};
let age_histograms = {};
let number_cases;
let time_chart = {};

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
  fetchData(url, '/time_chart')
}, 10000);

let currentScrollPosition = 0;

async function fetchData(url, endpoint) {

    currentScrollPosition = window.pageYOffset;

    const response = await fetch(`${url}${endpoint}`);
    const data = await response.json();

    window.scrollTo(0, currentScrollPosition);

    if (endpoint === '/time_chart') {
        console.log(data)
        drawTimeChart(data.time_a, data.active_cases, data.time_r, data.recovered_cases, data.time_d, data.death_cases, 'active');
    }
    

    if (endpoint === '/chart_provinces') {
        drawProvinceChart(data.provinces, data.active, 'active');
        drawProvinceChart(data.provinces, data.deaths, 'deaths');
        drawProvinceChart(data.provinces, data.recovered, 'recovered');
    }

    if (endpoint === '/age_histogram') {
        drawAgeHistogram(data.age_groups, data.active, 'active')
        drawAgeHistogram(data.age_groups, data.deaths, 'deaths')
        drawAgeHistogram(data.age_groups, data.recovered, 'recovered')
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
        document.getElementById('mean-age-infected').innerHTML = data.mean_age_infected;
        document.getElementById('mean_blood_pressure_infected').innerHTML = data.mean_blood_pressure_infected;
        document.getElementById('mean_heart_rate_infected').innerHTML = data.mean_heart_rate_infected;
        document.getElementById('mean_oxygen_saturation_infected').innerHTML = data.mean_oxygen_saturation_infected;
        document.getElementById('death_rate').innerHTML = `${data.death_rate}%`
        document.getElementById('recovery-rate').innerHTML = `${data.recovery_rate}%`
        document.getElementById('mean-temperature-infected').innerHTML = `${data.mean_temperature_infected}℃`
        document.getElementById('std-temperature-infected').innerHTML = `${data.std_temperature_infected}℃`
    }


}

function drawTimeChart(activeLabels, activeData, recoveredLabels, recoveredData, deathLabels, deathData, chartKey) {
    const ctx = document.getElementById(`time-chart-${chartKey}`).getContext('2d');

    destroyChart(time_chart[chartKey]);

    time_chart[chartKey] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: activeLabels, // Użyj etykiet aktywnych przypadków jako etykiet dla wykresu
            datasets: [{
                label: 'Active Cases',
                data: activeData,
                borderColor: 'blue',
                borderWidth: 2
            }, {
                label: 'Recovered Cases',
                data: recoveredData,
                borderColor: 'green',
                borderWidth: 2
            }, {
                label: 'Death Cases',
                data: deathData,
                borderColor: 'red',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    stacked: true
                }
            }
        }
    });
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

function drawAgeHistogram(labels, data, chartKey) {
    const ctx = document.getElementById(`age-chart-${chartKey}`).getContext('2d');

    destroyChart(age_histograms[chartKey])
    
    age_histograms[chartKey] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
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


function drawProvinceChart(labels, data, chartKey) {
    const ctx = document.getElementById(`province-chart-${chartKey}`).getContext('2d');

    destroyChart(provinces_histograms[chartKey]);
    
    provinces_histograms[chartKey] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Aktywne przypadki Covida',
                data: data,
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
