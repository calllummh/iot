"use strict";

// Firebase Configuration
var firebaseConfig = {
    apiKey: "AIzaSyDpE2uZyh7Pmk-nw0Mz3g3apr8UYQZ80mU",
    authDomain: "https://siotch.web.app",
    databaseURL: "https://siotch-default-rtdb.europe-west1.firebasedatabase.app/",
    projectId: "siotch"}

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var database = firebase.database();

// DOM Elements
var archSelect = document.getElementById("arch-select");
var pm25ChartElem = document.getElementById("pm25-chart");
var temperatureChartElem = document.getElementById("temperature-chart");
var humidityChartElem = document.getElementById("humidity-chart");

// Initialize Charts
function initChart(label, yAxisLabel) {
    return new Chart(document.getElementById(label), {
        type: "line",
        data: {
            labels: [], // Timestamps
            datasets: [{
                label: yAxisLabel,
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Timestamp" } },
                y: { title: { display: true, text: yAxisLabel } }
            }
        }
    });
}

var pm25Chart = initChart("pm25-chart", "PM2.5 (µg/m³)");
var temperatureChart = initChart("temperature-chart", "Temperature (°C)");
var humidityChart = initChart("humidity-chart", "Humidity (%)");

// Event Listener for Arch Selection
archSelect.addEventListener("change", function () {
    var arch = archSelect.value;
    if (arch) {
        loadData(arch);
    } else {
        clearCharts();
    }
});

// Load Data for Selected Arch
function loadData(arch) {
    var refPath = "air_quality";
    var ref = database.ref(refPath);
    ref.orderByChild("arch").equalTo(arch).on("value", function (snapshot) {
        if (snapshot.exists()) {
            var data = snapshot.val();
            var timestamps = [];
            var pm25Values = [];
            var temperatureValues = [];
            var humidityValues = [];

            Object.keys(data).forEach(function (key) {
                var entry = data[key];
                timestamps.push(entry.timestamp);
                pm25Values.push(entry.pm25);
                temperatureValues.push(entry.temperature);
                humidityValues.push(entry.humidity);
            });

            updateChart(pm25Chart, timestamps, pm25Values, "PM2.5 (µg/m³)");
            updateChart(temperatureChart, timestamps, temperatureValues, "Temperature (°C)");
            updateChart(humidityChart, timestamps, humidityValues, "Humidity (%)");
        } else {
            clearCharts();
        }
    });
}

// Update Chart with New Data
function updateChart(chart, labels, data, label) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.data.datasets[0].label = label;
    chart.update();
}

// Clear All Charts
function clearCharts() {
    [pm25Chart, temperatureChart, humidityChart].forEach(function (chart) {
        chart.data.labels = [];
        chart.data.datasets[0].data = [];
        chart.data.datasets[0].label = "";
        chart.update();
    });
}
